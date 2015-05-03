import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
import numpy as np
import StringIO
import re

from las import LASReader
from hacksaw import *

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
        f = self.request.POST['file']


        # Read the LAS file and create an las instance
        d = LASReader.from_text(f.value, unknown_as_other=False)

                
        c = get_aliases(d.curves.names)
        
            
        dict_to_pass = {d.curves.names[0]:list(d.data[d.curves.names[0]])}
        
        for k, v in c.items():
            dict_to_pass[k] = list(d.data[v])
        
        j = json.dumps(dict_to_pass)
        j = re.sub(r'"(.+?)": ', r'\1:', j)

        template_values = {
            'data': j,
            'well': d.well.WELL.data,
        }

        template = JINJA_ENVIRONMENT.get_template('view.html')
        self.response.write(template.render(template_values))


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
