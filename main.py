import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from las import LASReader

import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        file = self.request.POST['file']
        self.response.headers['Content-Type'] = "text/plain"
        las = LASReader(file.value, null_subs=np.nan, unknown_as_other=False)
        self.response.write(las.curves.names)

class UploadHandler(webapp2.RequestHandler):
  def post(self):
    file = self.request.POST['file']
    self.response.headers['Content-Type'] = "text/plain"

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render())
        
class ViewHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('view.html')
        self.response.write(template.render())
        

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/about', AboutHandler),
    ('/view', ViewHandler),
    ('/upload', UploadHandler)
], debug=True)
