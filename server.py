import webapp2
from google.appengine.ext import db
from httplib import *
from urllib2 import urlopen
import HTMLParser
import re
from threading import Thread
import Queue
from bs4 import BeautifulSoup
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import ndb
import os

q = Queue.Queue()

parser = HTMLParser.HTMLParser()

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
    headline = ndb.StringProperty(indexed=False)
    link = ndb.StringProperty()
    image = ndb.StringProperty(indexed=False)
    image_citation = ndb.StringProperty(indexed=False)
    source = ndb.StringProperty()
    team = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
    # Article consists of:
    #   headline
    #   link
    #   image
    #   source (BR, ESPN, etc)
    #   team
    
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
        except (HTTPException, IOError):
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
    article_list = []
    team_query = Team.query((Team.league == league), ancestor=team_key(DEFAULT_TEAM_NAME))
    team_entity = team_query.fetch(None)
    for team in team_entity:
        links = []
        del article_list[:]
        for site in team.sites:
            links.append(site.url)
        
        for link in links:
            per_site_counter = 0
            data = ''
            try:
                f = urlopen(link)
                data = f.read()
            except (HTTPException, IOError):
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
            for tag in reversed(soup.find_all(True)):
                try:
                    class_val = tag['class']
                    # article_info = [headline, link_url, image_url, image_cite]
                    article_info = []
                    #articles.append((class_val, len(class_val)))
                    if len(class_val) == 1:
                        if article_class in class_val:
                            article_info = normalize_article(tag)
                            if article_info[1] is not '':
                                check_and_put(article_info, domain, team, article_list)

                    elif 'bleacherreport' in link:
                        if article_class in class_val:
                            article_info = normalize_article(tag)
                            if article_info[1] is not '':
                               check_and_put(article_info, domain, team, article_list)
                except (KeyError, UnicodeDecodeError):
                    pass
            #break
        #break
    #articles_query = Article.query(ancestor=article_key(DEFAULT_ARTICLE_NAME)).order(-Article.date)
    #article_list = articles_query.fetch(10)
    return article_list
    
def check_and_put(article_info, domain, team, article_list):
    # extract from info list
    article = Article(parent=article_key(DEFAULT_ARTICLE_NAME))
    article.headline = article_info[0]
    article.link = article_info[1]
    article.image = article_info[2]
    article.image_citation = article_info[3]
    article.source = domain
    article.team = team.name

    # check if we already put in datastore
    article_query = Article.query(Article.link == article.link, ancestor=article_key(DEFAULT_ARTICLE_NAME))  
    num_matches = article_query.count(1)
    if num_matches > 0:
        # if we did, then don't put again
        pass
    else:
        # if we haven't, then make entity put
        article_list.append(article.headline)
        article.put()

def normalize_article(tag):
    tag.name = 'div'
    tag['class'] = 'post'
    tag_soup = BeautifulSoup(str(tag))
    link_tag = ''
    link_url = ''
    # get a link (hopefully the article link)
    for sub_tag in tag_soup.find_all(True):
        if sub_tag.name == 'a':
            link_tag = sub_tag
            break
    
    try:
        if len(str(link_tag['href']).strip()) == 0:
            pass
        # until we figure out what to do with tweets, don't store them
        if 'twitter' in str(link_tag['href']):
            return ['','','','']
    except (KeyError, TypeError):
        return ['','','','']
    # make sure link opens in new tab
    link_tag['target'] = '_blank'
    link_url = link_tag['href']
    
    headline = unicode()
    image = ''
    image_url = ''
    image_cite = ''
    try:
        # link
        #link_tag = tag.find_all('a')[0]
        # headline
        text_tags = tag.find_all(has_text)
        text_list = []
        for text_tag in text_tags:
            text_list.append(text_tag.string)
            #headline += text_tag.string
        text_list = sorted(text_list, key=len, reverse=True)
        i = 1
        headline = text_list[0]
        while len(headline) > 123:
            headline = text_list[i]
            i += 1
        
        # image
        image = tag_soup.find('img')
            
        image_url = ''
        if image is None:
            image = ''
        # need to extract deferred image loading link
        # then fix link so it works (width and height params screw everything up)
        else:
            image_soup = ''
            try:
                image['class'] = 'post-image'
                image['src'] = image['data-defer-src']
                image_soup = BeautifulSoup(str(image))
            except (KeyError, TypeError):
                # either this is N/A (KeyError)
                # or there was no img tag so image is None (TypeError)
                pass
            if image_soup is not '':
                try: 
                    cite_div = image_soup.find_all('div')[0]
                    image_cite = cite_div.string
                except (IndexError):
                    # no citation div tag
                    image_cite = ''
                    pass
        try:
            image_url = image['src']
        except TypeError:
            # if there was not an image
            pass
        
    except IndexError:
        pass
    # create new html (wrap link, headline, image in div)
    # if link is a tweet maybe put in different class of div?
    link_tag.string = headline
    new_tag = unicode('<div class="post">')
    new_tag += unicode(image_url)
    new_tag += unicode('<br>')
    new_tag += unicode(image_cite)
    new_tag += unicode('<br>')
    #new_tag += unicode(image)
    #new_tag += unicode(link_tag)
    new_tag += unicode(link_url)
    new_tag += unicode('<br>')
    new_tag += unicode(headline)
    #new_tag += unicode('<br>')
    #new_tag += headline
    #new_tag += unicode(image)
    new_tag += unicode('</div>')
    
    #probably should just store link_tag and image
    # then we can construct the stuff later
    # and maybe store headline separately?
    
    # Article consists of:
    #   headline
    #   link
    #   image
    #   source (BR, ESPN, etc)
    #   team
    #   id (hashed something... link?)
    
    return [headline, link_url, image_url, image_cite]

def has_text(tag):
    return tag.string is not None

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
            user_query = User.query((User.user == user), ancestor=user_key(DEFAULT_USER_NAME))
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
      
        articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME)).order(-Article.date)
        #articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME))
        article_list = articles_query.fetch(20)

        login_url = users.create_login_url('/')
        
        # output
        
        template_values = {
            'login' : login_url,
            'articles' : article_list
        }
        
        render_template(self, 'search.html', template_values)      
        """
        #self.response.out.write(header)
        
        for article in article_list:
            self.response.out.write('<div class="post">')
            self.response.out.write(article.headline)
            self.response.out.write('</div>')
            self.response.out.write('<br>')
            
        #self.response.out.write(footer)
        """

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
        
        if curr_user:
            logout_url = users.create_logout_url('/')
            name = curr_user.nickname()
            
            user_query = User.query((User.user == curr_user), ancestor=user_key(DEFAULT_USER_NAME))
            user = user_query.get()
            
            for i, team in enumerate(user.teams) :
                if i == 0 :
                    given_team = team.name
                user_teams.append(team.name)
            
            team = str(user_teams[0])
            
            articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME)).order(-Article.date)
            #articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME))
            article_list = articles_query.fetch(20)

            
        else:
            login_url = users.create_login_url('/')
            self.redirect('/')
          
        template_values = {
            'login' : login_url,
            'logout' : logout_url,
            'nickname' : name,
            'given_team' : given_team,
            'user_teams' : user_teams,
            'articles' : article_list
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
            
            for i, team in enumerate(user.teams) :
                team = user.teams[i]
                user_teams.append(team.name)
            
            team = str(given_team)
            
            articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME)).order(-Article.date)
            #articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME))
            article_list = articles_query.fetch(20)
                      
          
        else:
            login_url = users.create_login_url('/')
            
          
        template_values = {
            'login' : login_url,
            'logout' : logout_url,
            'nickname' : name,
            'given_team' : given_team,
            'user_teams' : user_teams,
            'articles' : article_list
        }        
        
        render_template(self, 'userPro.html', template_values)
    

class ChooseTeams(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-type'] = 'text/html'
        
        user = users.get_current_user()
        
        login_url = ''
        logout_url = ''
        
        name = ''
        user_teams = []
        
        if user:
            user_query = User.query((User.user == user), ancestor=user_key(DEFAULT_USER_NAME))
            user_db = user_query.get()
            
            if user_db == None:
                logout_url = users.create_logout_url('/')
                name = user.nickname()
                
                user_db = User(parent=user_key(DEFAULT_USER_NAME))
                user_db.user = user
                user_db.teams = []
                user_db.put()
            else:
                # check memcache first!
                user_teams = memcache.get(user.user_id())
                # if memcache is empty, pull from datastore
                if user_teams is None:
                    user_teams = user_db.teams
                    memcache.add(user.user_id(), user_teams, 300)
        else:
            login_url = users.create_login_url('/')
            self.redirect('/')
          
        template_values = {
            'login' : login_url,
            'logout' : logout_url,
            'nickname' : name,
            'teams' : user_teams
        }        
        
        render_template(self, 'editPro.html', template_values)
    
    def post(self):
        teams_str = self.request.get("userTeams")
        teams_str = teams_str[:-1]
        teams = teams_str.split('-')
        
        curr_user = users.get_current_user()
        
        user_query = User.query((User.user == curr_user), ancestor=user_key(DEFAULT_USER_NAME))
        user = user_query.get()
        
        if user == None:
            user = User(parent=user_key(DEFAULT_USER_NAME))
        
        num = 0        
        while num < len(teams) :
            team = UserTeam(parent=user_key(DEFAULT_USER_NAME))
            team.league = teams[num]
            team.name = teams[num + 1]
            
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
        article_list = get_articles('nfl')
        #"""
        self.response.out.write('<html><body>')
        for article in article_list:
            self.response.out.write(article)
        self.response.out.write('</body></html>')
        #"""
        
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

# ----------  AJAX -------------------------- #
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

class UpdateCache(webapp2.RequestHandler):
    def post(self):
        teams_str = self.request.get("userTeams")
        teams_str = teams_str[:-1]
        teams = teams_str.split(',')
        user_teams = []
        
        num = 0
        while num < len(teams) :
            # parent=user_key(DEFAULT_USER_NAME)
            team = UserTeam()
            team_and_league = teams[num].split('-')
            team.league = team_and_league[0]
            team.name = team_and_league[1]
            
            user_teams.append(team)
            
            num = num + 1
            
        user = users.get_current_user()
        
        if user:
            data = memcache.get(user.user_id())
            
            if data is not None:
                memcache.delete(user.user_id())
            
            memcache.set(user.user_id(), user_teams)
            
class SaveUserTeams(webapp2.RequestHandler):
    def post(self):
        teams_str = self.request.get("userTeams")
        teams_str = teams_str[:-1]
        teams = teams_str.split(',')
        
        curr_user = users.get_current_user()
        
        user_query = User.query((User.user == curr_user), ancestor=user_key(DEFAULT_USER_NAME))
        user = user_query.get()
        
        if user == None:
            user = User(parent=user_key(DEFAULT_USER_NAME))
        
        user.teams = []
        
        num = 0        
        while num < len(teams) :
            team = UserTeam(parent=user_key(DEFAULT_USER_NAME))
            team_and_league = teams[num].split('-')
            team.league = team_and_league[0]
            team.name = team_and_league[1]
            
            user.teams.append(team)
            
            num = num + 1
        
        user.put()
        
        memcache.delete(curr_user.user_id())
        memcache.set(curr_user.user_id(), user.teams)
        
        self.redirect('/feed')
        
class getMoreArticles(webapp2.RequestHandler):
    def post(self):
        offset = self.request.get('offset')
        # need offset to be an int
        offset = int(offset)
        team = self.request.get('team')

        articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME)).order(-Article.date)
        #articles_query = Article.query((Article.team == team), ancestor=article_key(DEFAULT_ARTICLE_NAME))
        article_list = articles_query.fetch(offset + 21)
        
        article_list = article_list[:-21]
        for i in range(0, len(article_list)):
            article = article_list[i]
            article.headline = article.headline.strip()

        template_values = {
            'articles' : article_list
        }
        
        article_template = 'templates/JSON/article_template.json'
        
        render_template(self, article_template, template_values) 
            
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/search', SearchQuery),
    ('/feed', Feed),
    ('/choose_teams', ChooseTeams),
    ('/teamsAjax', GetTeams),
    ('/updateCache', UpdateCache),
    ('/saveTeams', SaveUserTeams),
    ('/getMoreArticles', getMoreArticles),
    ('/getNFLSites', GetNFLSites),
    ('/getNBASites', GetNBASites),
    ('/getNHLSites', GetNHLSites),
    ('/getMLBSites', GetMLBSites),
    ('/getNFLArticles', GetNFLArticles),
    ('/getNBAArticles', GetNBAArticles),
    ('/getNHLArticles', GetNHLArticles),
    ('/getMLBArticles', GetMLBArticles)
], debug=True)