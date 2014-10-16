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
      


      self.response.out.write(str(articles))



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

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/search', SearchQuery)
], debug=True)