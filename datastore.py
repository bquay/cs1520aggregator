import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_TEAM_NAME = 'default_team'

def team_key(team_name=DEFAULT_TEAM_NAME):
	"""creates a Datastore key for a Team entity with team_name"""
	return ndb.Key('Team', team_name);

class Team(ndb.Model):
	league = ndb.StringProperty(indexed=False)
	name = ndb.StringProperty(indexed=False)

DEFAULT_ARTICLE_NAME = 'default_article'

def article_key(article_name=DEFAULT_ARTICLE_NAME):
    return ndb.Key('Article', article_name)

class Article(ndb.Model):
    title = ndb.StringProperty()
    source = ndb.StringProperty()
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

