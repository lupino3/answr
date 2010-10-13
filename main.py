import random
import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from models import Answr

class MainApp(webapp.RequestHandler):
    lang_strings = {
        "en" : {
            "lang"  : "en",
            "title" : "answr.it (BETA) - You can ask him everything",
            "type_your_question" : "Type your question",
            "must_ask" : "You must ask something!",
            "get_answer" : "Get your answer from answr.it!",
            "loading" : "Loading",
            "restart" : "Please click to restart"
        },
        "it" : {
            "lang"  : "it",
            "title" : "answr.it (BETA) - Chiedi qualsiasi cosa!",
            "type_your_question" : "Scrivi la tua domanda",
            "must_ask" : "Devi chiedere qualcosa!",
            "get_answer" : "Fai la tua domanda ad answr.it!",
            "loading" : "Caricamento",
            "restart" : "Fai clic per ricominciare"
        }
    }
    def get(self):
        try:
            l = self.get_main_language(self.request.headers['Accept-Language'])
            language_strings = MainApp.lang_strings[l]
            
        except Exception, e:
            logging.warning("Errror during language detection: %s - switching back to en" % str(e))
            language_strings = MainApp.lang_strings["en"]

        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        self.response.out.write(template.render(template_path, language_strings))

    def get_main_language(self, accept_language):
        # TODO: correctly handle a list of languages instead of a single main
        # language
        """The Accept-Language header is composed by a string like this: da,
        en-gb;q=0.8, en;q=0.7. We need the language that has the highest q
        value. If no q value is specified, 1 is implied."""
        logging.info("Trying to detect language from: %s" % accept_language)
        languages = accept_language.split(',')
        language = ("en", 0)
        for l in languages:
            q = 1
            if ';' in l:
                current_lang, q = l.split(';')
                q = float(q.split('=')[1])
            else:
                current_lang = l

            if q > language[1]:
                language = (current_lang, q)
                logging.info("Up for language %s (%.2f)" % language)

        # We don't need the q value anymore
        language = language[0]

        # Get the main language, ignoring the variant
        if "-" in language:
            language = language.split('-')[0]

        return language

class AnswrApp(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        try:
            random_answr = Answr.get_random(self.request.get('lang'))
        except Exception, e:
            logging.warning('Failed to get parameter lang, switching back to default')
            random_answr = Answr.get_random()
        self.response.out.write(random_answr.to_json())

application = webapp.WSGIApplication([('/answr', AnswrApp), ('/', MainApp)], debug = True)

if __name__ == '__main__':
    run_wsgi_app(application)
