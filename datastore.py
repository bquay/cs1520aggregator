import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

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