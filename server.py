import webapp2
from google.appengine.ext import db
from httplib import *
from urllib import urlopen
from HTMLParser import HTMLParser
import re
from threading import Thread
import Queue
from bs4 import BeautifulSoup
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb
import os

q = Queue.Queue()

def render_template(handler, templatename, templatevalues):
    path = os.path.join(os.path.dirname(__file__), templatename)
    html = template.render(path, templatevalues)
    handler.response.out.write(html)

DEFAULT_TEAM_NAME = 'default_team'

def team_key(team_name=DEFAULT_TEAM_NAME):
	"""creates a Datastore key for a Team entity with team_name"""
	return ndb.Key('Team', team_name);

class Site(ndb.Model):
    url = ndb.StringProperty()

class Team(ndb.Model):
	league = ndb.StringProperty()
	name = ndb.StringProperty()
	sites = ndb.StructuredProperty(Site, indexed=False)


DEFAULT_ARTICLE_NAME = 'default_article'

def article_key(article_name=DEFAULT_ARTICLE_NAME):
    return ndb.Key('Article', article_name)

class Article(ndb.Model):
    metadata = ndb.StringProperty()
    team = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
DEFAULT_USER_NAME = 'default_user'

def user_key(user_name=DEFAULT_USER_NAME):
	"""creates a Datastore key for a User entity with user_name"""
	return ndb.Key('User', user_name)
	
class UserTeams(ndb.Model):
	user = ndb.UserProperty()
	teams = ndb.StructuredProperty(Team, repeated=True)

class ViewedArticles(ndb.Model):
	user = ndb.UserProperty()
	articles = ndb.StructuredProperty(Article, repeated=True)

class Favorites(ndb.Model):
	user = ndb.UserProperty()
	articles = ndb.StructuredProperty(Article, repeated=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-type'] = 'text/html'

        filename = 'index.html'
        
        f = open(filename, 'r')
        myresponse = f.read()
        
        user = users.get_current_user()
        
        login_url = ''
        logout_url = ''
        
        name = ''
        
        if user:
            logout_url = users.create_logout_url('/')
            name = user.nickname()
            """ check to see if they have chosen teams """
            user_query = UserTeams.query((UserTeams.user == user), ancestor=user_key(DEFAULT_USER_NAME))
            user_entry = user_query.fetch(1)

            if (user_entry):
                """ direct to feed """
                self.redirect('/feed')
            else:
                """ direct to choose teams """
                self.redirect('/choose_teams')
        else:
            login_url = users.create_login_url('/')
          
        template_values = {
            'login' : login_url,
            'logout' : logout_url,
            'nickname' : name
        }
        
        
        render_template(self, 'index.html', template_values)

class SearchQuery(webapp2.RequestHandler):

    def get(self):
        self.redirect('/')

    def post(self):
        self.search()

    def search(self):
       
        team = self.request.get("team")
        path = 'text_files/sports_sites/'
        filename = 'sports_sites.txt'
        sites = []
        with open(path + filename) as f:
            sites = f.readlines()
      
        for i, site in enumerate(sites):
            sites[i] = site.strip()
      
        # figure out which league to look in
        league = ''
        path = 'text_files/teams/'
        match = False
        files = os.listdir(path)
        for t in files:
            if t[0] == '.':
                break
            list_name = t[:str.find(t, '-')]
            with open(path + t) as f:
                teams = f.readlines()
            for option in teams:
                if team == option.strip():
                    match = True
                    break
            if match:
                league = list_name
                break
    
        links_dict = self.get_team_links(sites, team, league)
      
        # ok we have the team pages 
        # should probably store them and then just retrieve them from datastore
        # for future calls
        links = []
        for entry in links_dict:
            # link might already be absolute, don't add domain if that's the case
            if '.com' in links_dict[entry]:
                link_parts = links_dict[entry].split('.com')
                links.append(entry + link_parts[1])
            else:
                links.append(entry + links_dict[entry])
          
        # get articles
        articles = self.get_articles(links)
      
      
        template_values = {
            'articles' : articles
        }
      
        # output
        filename = 'search_header.html'
        f = open(filename, 'r')
        header = f.read()
        f.close()
        
        filename = 'search_footer.html'
        f = open(filename, 'r')
        footer = f.read()
        f.close()
        
        #render_template(self, 'search.html', template_values)      
          
        self.response.out.write(header)
        
        for article in articles:
            self.response.out.write(article)
            self.response.out.write('<br>')
            
        self.response.out.write(footer)
        
      
    def get_team_links(self, sites, team, league):
    
        team = str(team)
        # split team into location and mascot
        if len(team.split(' ')) == 2:
            location = team[:str.find(team, ' ')]
            mascot = team[str.find(team, ' '):].strip()
        else:
            location = team[:str.find(team, ' ')]
            location += ' ' + team[str.find(team, ' '):str.rfind(team, ' ')].strip()
            mascot = team[str.rfind(team, ' '):].strip()
        #"""
      
        # lower case mascots and locations
        location = location.lower()
        mascot = mascot.lower()
        links_dict = {}
        # use urllib to get html
        for site in sites:
            url = site + '/' + league + '/teams'
            data = ''
            try:
                f = urlopen(url)
                #site = f.geturl()
                data = f.read()
            except HTTPException:
                data = ''
    
            # use bs to find some stuff
            soup = BeautifulSoup(data)
      
            all_links = soup.find_all('a')
            text = []
            links_team_filter = []
            the_link = ''
            for link in all_links:
                try:
                    if 'team' in str(link['href']):
                        links_team_filter.append(link)
                except (KeyError, UnicodeEncodeError):
                    pass
        
            # if the mascot is in the link text, then we want it
            for link in links_team_filter:
                try:
                    if mascot in str(link.text).lower():
                        the_link = str(link['href'])
                except (KeyError, UnicodeEncodeError):
                    pass

            # if not found in previous step, look for location in link text
            if the_link == '':
                for link in links_team_filter:
                    try:
                        if location in str(link.text).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                        pass
                
            # if the mascot is in the link text, then we want it
            if the_link == '':
                for link in all_links:
                    try:
                        if mascot in str(link.text).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                         pass

            # if not found in previous step, look for location in link text
            if the_link == '':
                for link in all_links:
                    try:
                        if location in str(link.text).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                        pass
                
            # still none found? Well... look at the href values
            # for mascot
            if the_link == '':
                for link in all_links:
                    try:
                        if mascot in str(link['href']).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                        pass
            # and then for location, with dashes replacing spaces
            if the_link == '':
                for link in all_links:
                    try:
                        if location.replace(' ', '-') in str(link['href']).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                        pass
                  
            links_dict[site] = the_link
            #"""
        return links_dict
    
    def get_articles(self, links):
    
        """
        Search Table
        ESPN : class="result"
        SI :   class="list-item"
        BR : "article" in tag["class"]

        """
        article_keys = {'espn': 'result', 'si': 'list-item', 'bleacherreport': 'block-list_item'}
        articles = []
        for link in links:
            per_site_counter = 0
            data = ''
            try:
                f = urlopen(link)
                data = f.read()
            except HTTPException:
                data = ''
    
            # use bs to find some stuff
            soup = BeautifulSoup(data)
        
            domain = link[link.find('.') + 1:link.rfind('.com')]
            article_key = ''
            try:
                article_key = article_keys[domain]
            except KeyError:
                continue
          
            article_key = unicode(article_key)
            #articles.append(link)
            #articles.append(article_key)
            
            # get the tags corresponding to the keys
            if per_site_counter > 10:
                break
            for tag in soup.find_all(True):
                try:
                    class_val = tag['class']
                    #articles.append((class_val, len(class_val)))
                    if len(class_val) == 1:
                        if article_key in class_val:
                            articles.append(tag)
                            per_site_counter += 1
                    elif 'bleacherreport' in link:
                        if article_key in class_val:
                            articles.append(tag)
                            per_site_counter += 1
                except (KeyError, UnicodeDecodeError):
                    pass
            
            #articles += soup.find_all()
            
        return articles

class Feed(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-type'] = 'text/html'

        filename = 'userPro.html'
        
        f = open(filename, 'r')
        myresponse = f.read()
        
        user = users.get_current_user()
        
        login_url = ''
        logout_url = ''
        
        name = ''
        
        if user:
            logout_url = users.create_logout_url('/')
            name = user.nickname()
          
        else:
            login_url = users.create_login_url('/')
          
        template_values = {
            'login' : login_url,
            'logout' : logout_url,
            'nickname' : name
        }
        
        
        render_template(self, 'userPro.html', template_values)

class ChooseTeams(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-type'] = 'text/html'

        filename = 'editPro.html'
        
        f = open(filename, 'r')
        myresponse = f.read()
        
        user = users.get_current_user()
        
        login_url = ''
        logout_url = ''
        
        name = ''
        
        if user:
            logout_url = users.create_logout_url('/')
            name = user.nickname()
          
        else:
            login_url = users.create_login_url('/')
          
        template_values = {
            'login' : login_url,
            'logout' : logout_url,
            'nickname' : name
        }
        
        
        render_template(self, 'editPro.html', template_values)
    
    def post(self):
        team = self.request.get("team")
        league = self.request.get("league")
        
        userTeam = UserTeams(parent=user_key(DEFAULT_USER_NAME))
        
        userTeam.user = users.get_current_user()
        userTeam.league = league
        userTeam.team = team
        
        userTeam.put()
        
        self.redirect('/feed')
        
# CRON JOBS
class GetNFLSites(webapp2.RequestHandler):

    def get(self):
        self.search('nfl')

    def post(self):
        self.search('nfl')

    def search(self, league):
    
        path = 'text_files/sports_sites/'
        filename = 'sports_sites.txt'
        sites = []
        with open(path + filename) as f:
            sites = f.readlines()
      
        for i, site in enumerate(sites):
            sites[i] = site.strip()
      
        # figure out which league to look in
        path = 'text_files/teams/'
        match = False
        files = os.listdir(path)
        teams = []
        team_sites = {}
        for t in files:
            if t[0] == '.':
                break
            if league in t:
                with open(path + t) as f:
                    teams = f.readlines()
                break
        
        for i in range(len(teams)):
            teams[i] = teams[i].strip()
        
        i = 0
        for team in teams:
            team_sites[team] = self.get_team_links(sites, team, league)
            i += 1
            if i == 3:
                break
        
        team_entity = ''
        
        for team in team_sites:
            team_query = Team.query((Team.name == team), ancestor=user_key(DEFAULT_TEAM_NAME))
            team_entity = team_query.fetch(1)
            if len(team_entity) == 0:
                team_entity = Team(parent=user_key(DEFAULT_TEAM_NAME))
                team_entity.name = team
            else:
                team_entity = team_entity[0]
            for site in team_sites[team]:
                # put sites up
                parent=user_key(DEFAULT_USER_NAME)
                add_site = Site()
                add_site.url = site
                team_entity.sites = []
                team_entity.sites.append(add_site)
            team_entity.put()
        
        
        
        self.response.out.write('<html><body>')
        
        self.response.out.write(str(team_entity))
            
        self.response.out.write('</body></html>')
      
    def get_team_links(self, sites, team, league):
    
        team = str(team)
        # split team into location and mascot
        if len(team.split(' ')) == 2:
            location = team[:str.find(team, ' ')]
            mascot = team[str.find(team, ' '):].strip()
        else:
            location = team[:str.find(team, ' ')]
            location += ' ' + team[str.find(team, ' '):str.rfind(team, ' ')].strip()
            mascot = team[str.rfind(team, ' '):].strip()
       
      
        # lower case mascots and locations
        location = location.lower()
        mascot = mascot.lower()
        links_dict = {}
        # use urllib to get html
        for site in sites:
            url = site + '/' + league + '/teams'
            data = ''
            try:
                f = urlopen(url)
                #site = f.geturl()
                data = f.read()
            except HTTPException:
                data = ''
    
            # use bs to find some stuff
            soup = BeautifulSoup(data)
      
            all_links = soup.find_all('a')
            text = []
            links_team_filter = []
            the_link = ''
            for link in all_links:
                try:
                    if 'team' in str(link['href']):
                        links_team_filter.append(link)
                except (KeyError, UnicodeEncodeError):
                    pass
        
            # if the mascot is in the link text, then we want it
            for link in links_team_filter:
                try:
                    if mascot in str(link.text).lower():
                        the_link = str(link['href'])
                except (KeyError, UnicodeEncodeError):
                    pass

            # if not found in previous step, look for location in link text
            if the_link == '':
                for link in links_team_filter:
                    try:
                        if location in str(link.text).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                        pass
                
            # if the mascot is in the link text, then we want it
            if the_link == '':
                for link in all_links:
                    try:
                        if mascot in str(link.text).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                         pass

            # if not found in previous step, look for location in link text
            if the_link == '':
                for link in all_links:
                    try:
                        if location in str(link.text).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                        pass
                
            # still none found? Well... look at the href values
            # for mascot
            if the_link == '':
                for link in all_links:
                    try:
                        if mascot in str(link['href']).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                        pass
            # and then for location, with dashes replacing spaces
            if the_link == '':
                for link in all_links:
                    try:
                        if location.replace(' ', '-') in str(link['href']).lower():
                            the_link = str(link['href'])
                    except (KeyError, UnicodeEncodeError):
                        pass
                  
            links_dict[site] = the_link
        links = []
        for entry in links_dict:
            # link might already be absolute, don't add domain if that's the case
            if '.com' in links_dict[entry]:
                link_parts = links_dict[entry].split('.com')
                links.append(entry + link_parts[1])
            else:
                links.append(entry + links_dict[entry])
            
        return links
        
class GetNFLArticles(webapp2.RequestHandler):

    def get_articles(self, links):
    
        """
        Search Table
        ESPN : class="result"
        SI :   class="list-item"
        BR : "article" in tag["class"]

        """
        article_keys = {'espn': 'result', 'si': 'list-item', 'bleacherreport': 'block-list_item'}
        articles = []
        for link in links:
            per_site_counter = 0
            data = ''
            try:
                f = urlopen(link)
                data = f.read()
            except HTTPException:
                data = ''
    
            # use bs to find some stuff
            soup = BeautifulSoup(data)
        
            domain = link[link.find('.') + 1:link.rfind('.com')]
            article_key = ''
            try:
                article_key = article_keys[domain]
            except KeyError:
                continue
          
            article_key = unicode(article_key)
            #articles.append(link)
            #articles.append(article_key)
            
            # get the tags corresponding to the keys
            if per_site_counter > 10:
                break
            for tag in soup.find_all(True):
                try:
                    class_val = tag['class']
                    #articles.append((class_val, len(class_val)))
                    if len(class_val) == 1:
                        if article_key in class_val:
                            articles.append(tag)
                            per_site_counter += 1
                    elif 'bleacherreport' in link:
                        if article_key in class_val:
                            articles.append(tag)
                            per_site_counter += 1
                except (KeyError, UnicodeDecodeError):
                    pass
            
            #articles += soup.find_all()
            
        return articles
    
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/search', SearchQuery),
    ('/feed', Feed),
    ('/choose_teams', ChooseTeams),
    ('/getNFLSites', GetNFLSites),
    ('/getNFLArticles', GetNFLArticles)
], debug=True)