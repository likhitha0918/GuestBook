import os
import webapp2
import jinja2
from google.appengine.ext import ndb

# Set up Jinja environment for HTML templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

# Define the Message model in Datastore
class Message(ndb.Model):
    author = ndb.StringProperty()
    content = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

# Handler for the main page (guestbook)
class MainPage(webapp2.RequestHandler):
    def get(self):
        messages = Message.query().order(-Message.created).fetch()
        template = jinja_env.get_template('index.html')
        self.response.out.write(template.render(messages=messages))

# Handler for submitting a new message
class NewMessage(webapp2.RequestHandler):
    def post(self):
        author = self.request.get('author')
        content = self.request.get('content')

        if author and content:
            message = Message(author=author, content=content)
            message.put()
            self.redirect('/')
        else:
            error = "Please enter both your name and a message!"
            template = jinja_env.get_template('index.html')
            self.response.out.write(template.render(error=error))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', NewMessage)
], debug=True)
