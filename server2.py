import webapp2
from google.appengine.ext import db
from httplib import *
from urllib import *
from HTMLParser import HTMLParser
import sys
import os

isLink = 0

class MainPage(webapp2.RequestHandler):
      
    def get(self):
        # load teams from files
        file_dir = "text_files"
        files = os.listdir(file_dir)
        teams = dict()
        for file in files:
          list_name = file[:str.find(file, '-')]
          with open(file_dir + '/' + file) as f:
            teams[list_name] = f.readlines()
        
        self.response.headers['Content-type'] = 'text/html'
        # make selection buttons
        form_string = """<form method="post" action="search" id="league">
<select>
"""
        
        for entry in teams:
          form_string += '<option value="'
          #form_string += entry + '" id="'
          form_string += entry
          form_string += '">' + str.upper(entry) 
          form_string += '</option>'

        form_string += "</select>"

        myresponse = """
<html>
<head>
<script src="funcs.js">
</script>
</head>
<body>
"""
        
        myresponse += form_string
        myresponse += """
</body>
</html>       
"""
        self.response.out.write(myresponse)
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)