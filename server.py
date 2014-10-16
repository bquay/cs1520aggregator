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

DEFAULT_USER_NAME = 'default_user'

def user_key(user_name=DEFAULT_USER_NAME):
	"""creates a Datastore key for a User entity with user_name"""
	return ndb.Key('User', user_name)
	
class UserTeams(ndb.Model):
	user = ndb.UserProperty()
	league = ndb.StringProperty(indexed=False)
	team = ndb.StringProperty(indexed=False)

class ViewedArticles(ndb.Model):
	user = ndb.UserProperty()
	article = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class Favorites(ndb.Model):
	user = ndb.UserProperty()
	article = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

DEFAULT_TEAM_NAME = 'default_team'

def team_key(team_name=DEFAULT_TEAM_NAME):
	"""creates a Datastore key for a Team entity with team_name"""
	return ndb.Key('Team', team_name);

class Teams(ndb.Model):
	league = ndb.StringProperty(indexed=False)
	name = ndb.StringProperty(indexed=False)

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
		  user_query = UserTeams.query(ancestor=user_key(user_name))
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

        #self.response.out.write(myresponse)

class SearchQuery(webapp2.RequestHandler):

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
      
      
      # output
      self.response.out.write("<html><body>")
      


      self.response.out.write(str(team) + str(articles))



      self.response.out.write("</body></html>")
      
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
        articles.append(link)
        articles.append(article_key)
        
        # get the tags corresponding to the keys
        
        for tag in soup.find_all(True):
          try:
            class_val = tag['class']
            articles.append((class_val, len(class_val)))
            if len(class_val) == 1:
              if article_key in class_val:
                articles.append(tag)
            elif 'bleacherreport' in link:
              if article_key in class_val:
                articles.append(tag)
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
		team = self.response.get("team")
		league = self.response.get("league")
		
		user_name = self.request.get('user_name', DEFAULT_USER_NAME)
		
		userTeam = UserTeams(parent=user_key(user_name))
		
		userTeam.user = users.get_current_user()
		userTeam.league = league
		userTeam.team = team
		
		userTeam.put()
		
		self.redirect('/feed')
	
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/search', SearchQuery),
	('/feed', Feed),
	('/choose_teams', ChooseTeams)
], debug=True)