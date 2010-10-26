from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Question, Answr
from utils import detect_language_from_msg

class XMPPHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        try:
            question = " ".join([x for x in message.body.split() if not x.startswith('@')])
            lang, confidence = detect_language_from_msg(question)
        except:
            logging.warning("Error during language detection. Switching back to en")
            lang = "en"

        answr = Answr.answr(lang).text
        Question.save(message.body, answr, 'xmpp', message.sender, lang)
        message.reply(answr)

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
