import random
import logging
import os

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from models import Question, Answr

class MainApp(webapp.RequestHandler):
    lang_strings = {
        "en" : {
            "lang"  : "en",
            "title" : "answr.it (BETA) - You can ask him everything",
            "type_your_question" : "Type your question",
            "get_answer" : "Get your answer from answr.it!",
            "loading" : "Loading",
            "restart" : "Please click to restart",
            "i_asked" : "I asked to answr",
            "and_he_replied" : "and he replied",
            "ask_again" : "Ask another question!",
            "share" : "Share"
        },
        "it" : {
            "lang"  : "it",
            "title" : "answr.it (BETA) - Chiedi qualsiasi cosa!",
            "type_your_question" : "Scrivi la tua domanda",
            "get_answer" : "Fai la tua domanda ad answr.it!",
            "loading" : "Caricamento",
            "restart" : "Fai clic per ricominciare",
            "i_asked" : "Ho chiesto ad answr",
            "and_he_replied" : "e lui mi ha risposto",
            "ask_again" : "Chiedi ancora!",
            "share" : "Condividi"
        }
    }
    
    def detect_language(self):
        """Returns the list of strings to be used for the detected language"""
        l = None

        # 1. If a language was specified in GET, use that language
        if self.request.get('lang'):
            l = self.request.get('lang')
            logging.info('Language %s passed via GET' % l)

        # 2. If no language was specified, get it from cookies
        elif self.request.cookies.get('answrlang'):
            l = self.request.cookies.get('answrlang')
            logging.info('Language %s passed via cookies' % l)

        # 3. If no cookies, try to detect
        else:
            try:
                l = self.get_main_language(self.request.headers['Accept-Language'])
            except Exception, e:
                logging.warning("Error during language detection: %s - switching back to en" % str(e))
                l = "en"

        # Try to get strings for the detected language
        try:
            language_strings = MainApp.lang_strings[l]
        except Exception, e:
            logging.warning("Error during language detection: %s - switching back to en" % str(e))
            l = "en"
            language_strings = MainApp.lang_strings[l]

        return (l, language_strings)

    def get(self):
        language, language_strings = self.detect_language()
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'answr.html')

        # Save to a cookie the detected language
        self.response.headers.add_header('Set-Cookie', 'answrlang=%s' % language)

        # Output the response
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

        # Please, browser, don't cache my answrs!
        self.response.headers['Pragma'] = 'no-cache'
        try:
            # The JS code should pass me the language
            lang = self.request.get('lang')
        except Exception, e:
            logging.warning('Failed to get parameter lang, switching back to default')
            lang = "en"

        random_answr = Answr.answr(lang)
        q_text = self.request.get('question')
        question_id = Question.save(q_text, random_answr.text, tech = 'web', lang = lang, who = str(self.request.remote_addr))
        logging.info("Question saved. ID: " + str(question_id))
        
        json_response = '{"text" : "%s", "q_id" : "%d", "q_text": "%s"}' % (random_answr.text, question_id, q_text)
        self.response.out.write(json_response)

class QuestionApp(webapp.RequestHandler):
    def get(self):
        try:
            q = int(self.request.get('id'))
            logging.info('Question ID: %d' % q)
            question = Question.get_by_id(q)

            # Using the language of the question
            template_strings = MainApp.lang_strings[question.lang]
            template_strings['question'] = question.text
            template_strings['answr'] = question.answr
            template_strings['q_id'] = q
            logging.info("%s -> %s" % (question.text, question.answr))

            template_path = os.path.join(os.path.dirname(__file__), 'templates', 'answr.html')

            # Output the response
            self.response.out.write(template.render(template_path, template_strings))
        except Exception, e:
            logging.warning('Something went wrong with question permalink: %s' % str(e))
            self.redirect('/')

application = webapp.WSGIApplication([('/answr', AnswrApp), ('/', MainApp), ('/q', QuestionApp)], debug = True)

if __name__ == '__main__':
    run_wsgi_app(application)
