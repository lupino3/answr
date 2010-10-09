import random

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Answr

class AnswrApp(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        random_answr = Answr.get_random()
        self.response.out.write(random_answr.to_json())

application = webapp.WSGIApplication([('/answr', AnswrApp)], debug = True)

if __name__ == '__main__':
    run_wsgi_app(application)
