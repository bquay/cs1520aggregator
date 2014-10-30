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
	sites = ndb.LocalStructuredProperty(Site, indexed=False, repeated=True)


DEFAULT_ARTICLE_NAME = 'default_article'

def article_key(article_name=DEFAULT_ARTICLE_NAME):
    return ndb.Key('Article', article_name)

class Article(ndb.Model):
    metadata = ndb.TextProperty(indexed=False)
    team = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
DEFAULT_USER_NAME = 'default_user'

def user_key(user_name=DEFAULT_USER_NAME):
	"""creates a Datastore key for a User entity with user_name"""
	return ndb.Key('User', user_name)
	
class UserTeam(ndb.Model):
    league = ndb.StringProperty(indexed=False)
    name = ndb.StringProperty()

class User(ndb.Model):
	user = ndb.UserProperty()
	teams = ndb.LocalStructuredProperty(UserTeam, repeated=True)

class ViewedArticles(ndb.Model):
	user = ndb.UserProperty()
	articles = ndb.StructuredProperty(Article, repeated=True)

class Favorites(ndb.Model):
	user = ndb.UserProperty()
	articles = ndb.StructuredProperty(Article, repeated=True)

def search(league):

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
        team_sites[team] = get_team_links(sites, team, league)
        #i += 1
        if i == 4:
            break
    
    team_entity = ''
    entity_found = False
    info = []
    
    for team in team_sites:
        entity_found = False
        team_query = Team.query((Team.name == team), ancestor=team_key(DEFAULT_TEAM_NAME))
        team_entity = team_query.fetch(1)
        if len(team_entity) == 0:
            team_entity = Team(parent=team_key(DEFAULT_TEAM_NAME))
            team_entity.name = team
            team_entity.league = league
        else:
            entity_found = True
            team_entity = team_entity[0]
        team_entity.sites = []
        for site in team_sites[team]:
            # put sites up
            add_site = Site()
            add_site.url = site
            team_entity.sites.append(add_site)
        team_entity.put()
        info.append((team_entity, entity_found))        
        
    return info
    
def get_team_links(sites, team, league):

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
              
        links_dict[site] = str(the_link)
    links = []
    for entry in links_dict:
        # link might already be absolute, don't add domain if that's the case
        if '.com' in links_dict[entry]:
            link_parts = links_dict[entry].split('.com')
            links.append(entry + link_parts[1])
        else:
            links.append(entry + links_dict[entry])
        
    return links

def get_articles(league):

    """
    Search Table
    ESPN : class="result"
    SI :   class="list-item"
    BR : "article" in tag["class"]

    """
    article_classes = {'espn': 'result', 'si': 'list-item', 'bleacherreport': 'block-list_item'}
    articles = []
    team_query = Team.query((Team.league == league), ancestor=team_key(DEFAULT_TEAM_NAME))
    team_entity = team_query.fetch(None)

    for team in team_entity:
        links = []
        for site in team.sites:
            links.append(site.url)
        
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
            article_class = ''
            try:
                article_class = article_classes[domain]
            except KeyError:
                continue
      
            article_class = unicode(article_class)
            #articles.append(link)
            #articles.append(article_key)
        
            # get the tags corresponding to the keys
            for tag in soup.find_all(True):
                try:
                    class_val = tag['class']
                    #articles.append((class_val, len(class_val)))
                    if len(class_val) == 1:
                        if article_class in class_val:
                            # add article to data store
                            article = Article(parent=article_key(DEFAULT_ARTICLE_NAME))
                            article.metadata = str(tag)
                            article.team = team.name
                            article.put()
                    elif 'bleacherreport' in link:
                        if article_class in class_val:
                            # add article to data store
                            article = Article(parent=article_key(DEFAULT_ARTICLE_NAME))
                            article.metadata = str(tag)
                            article.team = team.name
                            article.put()
                except (KeyError, UnicodeDecodeError):
                    pass
        
    articles_query = Article.query(ancestor=article_key(DEFAULT_ARTICLE_NAME))
    article_list = articles_query.fetch(None)
    return testing

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
        league = self.request.get("league")
        league = league.lower()        
      
        #articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME)).order(-Article.date)
        articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME))
        article_list = articles_query.fetch(20)
      
        """
        template_values = {
            'articles' : articles
        }
        """
      
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
        
        for article in article_list:
            self.response.out.write('<div class="post">')
            self.response.out.write(article.metadata)
            self.response.out.write('</div>')
            self.response.out.write('<br>')
            
        self.response.out.write(footer)

class Feed(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-type'] = 'text/html'
        
        given_team = ''
        user_teams = []
        articles = []
        
        curr_user = users.get_current_user()
        
        login_url = ''
        logout_url = ''
        
        name = ''
        
        myresponse = ''
        
        if curr_user:
            logout_url = users.create_logout_url('/')
            name = curr_user.nickname()
            
            user_query = User.query((User.user == curr_user), ancestor=user_key(DEFAULT_USER_NAME))
            user = user_query.get()
            
            for team, i in enumerate(user.teams) :
                if i == 0 :
                    given_team = team.name
                user_teams.append(team.name)
            
            article_query = Article.query((Article.team == given_team), ancestor=article_key(DEFAULT_ARTICLE_NAME))
            article_objects = article_query.fetch(20)
            
            for article in article_objects :
                articles.append(article.metadata)                
          
        else:
            login_url = users.create_login_url('/')
          
        template_values = {
            'login' : login_url,
            'logout' : logout_url,
            'nickname' : name,
            'given_team' : given_team,
            'user_teams' : user_teams,
            'articles' : articles
        }        
        
        render_template(self, 'userPro.html', template_values)
        
    def post(self):
        self.response.headers['Content-type'] = 'text/html'
        
        given_team = self.request.get('team')
        
        user_teams = []
        articles = []
        
        curr_user = users.get_current_user()
        
        login_url = ''
        logout_url = ''
        
        name = ''
        
        if curr_user:
            logout_url = users.create_logout_url('/')
            name = curr_user.nickname()
            
            user_query = User.query((User.user == curr_user), ancestor=user_key(DEFAULT_USER_NAME))
            user = user_query.get()
            
            for team, i in enumerate(user.teams) :
                user_teams.append(team.name)
            
            article_query = Article.query((Article.team == given_team), ancestor=article_key(DEFAULT_ARTICLE_NAME))
            article_objects = article_query.fetch(20)
            
            for article in article_objects :
                articles.append(article.metadata)                
          
        else:
            login_url = users.create_login_url('/')
          
        template_values = {
            'login' : login_url,
            'logout' : logout_url,
            'nickname' : name,
            'given_team' : given_team,
            'user_teams' : user_teams,
            'articles' : articles
        }        
        
        render_template(self, 'userPro.html', template_values)
    

class ChooseTeams(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-type'] = 'text/html'
        
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
        teams_str = self.request.get("teamsToAdd")
        teams_str = teams_str[:-1]
        
        teams = teams_str.split('-')
        numTeams = len(teams) / 2
        
        user = User(parent=user_key(DEFAULT_USER_NAME))
        user.user = users.get_current_user()
        
        num = 0        
        while num < numTeams :
            team = Team(parent=user_key(DEFAULT_USER_NAME))
            team.league = teams[num]
            team.team = teams[num + 1]
            
            user.teams.append(team)
            
            num = num + 2
        
        user.put()
        
        self.redirect('/feed')
        
        
#--------------------------- CRON JOBS ----------------------------#
class GetNFLSites(webapp2.RequestHandler):
    def get(self):
        info = search('nfl')
        """
        self.response.out.write('<html><body>')
        self.response.out.write(str(info))
        self.response.out.write('</body></html>')
        """
    def post(self):
        info = search('nfl')
        
class GetNBASites(webapp2.RequestHandler):
    def get(self):
        info = search('nba')
        """
        self.response.out.write('<html><body>')
        self.response.out.write(str(info))
        self.response.out.write('</body></html>')
        """
    def post(self):
        info = search('nba')
        
class GetNHLSites(webapp2.RequestHandler):
    def get(self):
        info = search('nhl')
        """
        self.response.out.write('<html><body>')
        self.response.out.write(str(info))
        self.response.out.write('</body></html>')
        """
    def post(self):
        info = search('nhl')
        
class GetMLBSites(webapp2.RequestHandler):
    def get(self):
        info = search('mlb')
        """
        self.response.out.write('<html><body>')
        self.response.out.write(str(info))
        self.response.out.write('</body></html>')
        """
    def post(self):
        info = search('mlb')
                
class GetNFLArticles(webapp2.RequestHandler):

    def get(self):
        get_articles('nfl')
        """
        self.response.out.write('<html><body>')
        self.response.out.write(str(article_list))
        self.response.out.write('</body></html>')
        """
        
    def post(self):
        get_articles('nfl')      
class GetNBAArticles(webapp2.RequestHandler):

    def get(self):
        get_articles('nba')
        """
        self.response.out.write('<html><body>')
        self.response.out.write(str(article_list))
        self.response.out.write('</body></html>')
        """
    def post(self):
        get_articles('nba')
                
class GetNHLArticles(webapp2.RequestHandler):

    def get(self):
        get_articles('nhl')
        """
        self.response.out.write('<html><body>')
        self.response.out.write(str(article_list))
        self.response.out.write('</body></html>')
        """
        
    def post(self):
        get_articles('nhl')      
class GetMLBArticles(webapp2.RequestHandler):

    def get(self):
        testing = get_articles('mlb')
        #"""
        self.response.out.write('<html><body>')
        self.response.out.write(str(testing))
        self.response.out.write('</body></html>')
        #"""
    def post(self):
        get_articles('mlb')

class GetTeams(webapp2.RequestHandler):
    def post(self):
        league = self.request.get('league')
        json_file = 'templates/JSON/'
        
        if league == 'MLB' :
            json_file = json_file + 'mlb-teams.json'
        elif league == 'NBA':
            json_file = json_file + 'nba-teams.json'
        elif league == 'NFL':
            json_file = json_file + 'nfl-teams.json'
        elif league == 'NHL':
            json_file = json_file + 'nhl-teams.json'
        
        render_template(self, json_file, {})
    
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/search', SearchQuery),
    ('/feed', Feed),
    ('/choose_teams', ChooseTeams),
    ('/teamsAjax', GetTeams),
    ('/getNFLSites', GetNFLSites),
    ('/getNBASites', GetNBASites),
    ('/getNHLSites', GetNHLSites),
    ('/getMLBSites', GetMLBSites),
    ('/getNFLArticles', GetNFLArticles),
    ('/getNBAArticles', GetNBAArticles),
    ('/getNHLArticles', GetNHLArticles),
    ('/getMLBArticles', GetMLBArticles)
], debug=True)