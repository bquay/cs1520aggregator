import webapp2
from google.appengine.ext import db
from httplib import *
from urllib import urlopen
from HTMLParser import HTMLParser
import re
from threading import Thread
import Queue
from bs4 import BeautifulSoup

q = Queue.Queue()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-type'] = 'text/html'

        filename = 'index.html'
        
        f = open(filename, 'r')
        myresponse = f.read()

        self.response.out.write(myresponse)

class SearchQuery(webapp2.RequestHandler):

    def post(self):
      self.search()
      
    def find_site(self, team, league, main_site):
      
      html = self.get_html(main_site + '/' + league + '/teams')
      # look for whole team name, just location, and just mascot
      # return stuff around the locations
      # make sure we're dealing with strings
      team = str(team)
      html = str(html)
      
      # everything lower case for better matching
      team = str.lower(team)
      html = str.lower(html)
      
      # split the team name into two parts
      location = ''
      mascot = ''
      
      if len(team.split(' ')) == 2:
        location = team[:str.find(team, ' ')]
        mascot = team[str.find(team, ' '):].strip()
      else:
        location = team[:str.find(team, ' ')]
        location += ' ' + team[str.find(team, ' '):str.rfind(team, ' ')].strip()
        mascot = team[str.rfind(team, ' '):].strip()

      team_parts = team.split(' ')

      parser = League_parser(location, mascot)

      parser.feed(html)
      links = parser.links
      
      the_link = self.choose_link(links, location, league)
      
      # kind of terrible fix for SI problem
      if team_parts[-2] not in the_link and 'teams' not in the_link:
        the_link = '/nfl/team/'
        for part in team_parts:
          the_link += part
          if part is not team_parts[-1]:
            the_link += '-'
            
      # build out relative links
      # complete relative links
      if '.com' not in the_link:
        the_link = main_site + the_link
      q.put(the_link)

    # ok, how to choose which one
    # I think picking the shortest will probably work almost always
    # do this for now (a keyword check is probably a good idea, too)
    # measure shortest from the .com, to prevent the domain from being included
    def choose_link(self, links, location, league):
      the_link = ''
      i = 0
      links = sorted(links, key=len)
      try:
        the_link = links[0]
      except IndexError:
        pass
      
      return the_link


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
        
      team_sites = []
      threads = []
      # go to sites and find team page url
      for site in sites:
        threads.append(Thread(target=self.find_site, args = (team, league, site)))

      for thread in threads:
        thread.start()
        
      for thread in threads:
        thread.join()
            
      while q.empty() is not True:
        team_sites.append(q.get())

      threads = []
      # go and get the team pages
      for site in team_sites:
        #self.get_team_site(site)
        threads.append(Thread(target=self.get_team_site, args = (site,)))
               
      for thread in threads:
        thread.start()
      
      for thread in threads:
        thread.join()      

      # output
      self.response.out.write("<html><body>")
      


      self.response.out.write()



      self.response.out.write("</body></html>")
    
    def get_articles(self, parse_key, site, html):
      parser = Team_parser(parse_key, site)
      parser.feed(html)
      site_articles = parser.links
      return site_articles

    def get_team_site(self, site):
      data = self.get_html(site)
      q.put((site, data))
  
    def get_html(self, site):
      try:
        f = urlopen(site)
        data = f.read()
      except HTTPException:
        data = ''
      return data
      
class League_parser(HTMLParser):
  def __init__(self, location, mascot):
    HTMLParser.__init__(self)
    self.location = location
    self.mascot = mascot
    self.last_link = ''
    self.links = []    
  
  # essentially here we're looking for the location of the team in the web page
  # then going back to the last <a> tag (last_link) and adding it to the list
  # it works well, since most links look like: <a ...> Team </a>
  # of course, not all... It doesn't work for SI
  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      for name, value in attrs:
        if name == 'href':
          self.last_link = value
             
  def handle_data(self, data):
    if self.location in data:
      self.links.append(self.last_link)
    
class Team_parser(HTMLParser):
  def __init__(self, parse_key, site):
    HTMLParser.__init__(self)
    self.parse_keys = parse_key
    self.the_site = site
    self.in_content = False
    self.get_data = False
    self.links = [] 
    self.titles = []
    self.div_levels = 0
    
  # cheating a little bit, we know which element class to look in
  # using the parse_key dict, so get all links (and title values or
  # data value, if no title in <a> tag)
  def handle_starttag(self, tag, attrs):
    if tag == 'div':
      if self.in_content:
        self.div_levels += 1
      for name, value in attrs:
        if name == 'id' or name == 'class':
          if self.parse_keys[self.the_site] in value:
            self.in_content = True
            self.div_levels += 1
            
    if tag == 'a':
      self.get_data = True
      if self.in_content:
        for name, value in attrs:
          if name == 'href':
            self.links.append(value)
          if name == 'title':
            self.titles.append(value)
            self.get_data = False
  
  def handle_endtag(self, tag):
    if tag == 'div':
      self.div_levels -= 1
      if self.div_levels == 0:
        self.in_content = False

  def handle_data(self, data):
    if self.get_data:
      self.titles.append(data)
      self.get_data = False
  
  

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/search', SearchQuery)
], debug=True)