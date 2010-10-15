from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Question, Answr

class XMPPHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        answr = Answr.answr().text
        Question.save(message.body, answr, 'xmpp', message.sender, "en")
        message.reply(answr)

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
