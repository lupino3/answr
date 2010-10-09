from models import Answr
import logging
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class PopulatePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if not user:
            print "<a href = '%s'>Log in with your Google Account</a>" % users.create_login_url(self.request.path)
        elif users.is_current_user_admin():
            print "Populating the DB..."
            answrs = ["No", "Maybe", "Better luck next time", "You have to believe it", "Of course", "You will improve your situation",
                "Think slower", "Absolutely", "It is better to wait", "Keep it for yourself", "No space for doubts", "Be patient",
                "Be careful and keep watching", "You will be glad of doing it", "Keep it simple", "Keep improving yourself", "Don't ask anything more",
                "The best solution may not be the most obvious", "It is out of your control", "Watch your step", "Talk about it with a friend before doing anything",
                "Don't be shy", "It's a good moment for your projects", "Things will change around you", "It's important", "Don't wait",
                "You will not forget it", "Try to look around", "Take it easy", "You have to risk something", "You will need to know more about it", "You are not ojective",
                "Now you can", "It will make things more interesting", "It is not as sure as you might think", "It's not important", "Tell someone how important they are",
                "Open your mind", "Open your eyes", "Don't talk too much", "It's a good moment to start new projects", "You will get the desired result", "Somebody will help you",
                "Do it now", "Keep going", "Stop now, you can still limit damage", "Maybe it's easier than you thought", "Take your time", "Enjoy yourself", "Listen more carefully, and you will understand", "Only you know the answer", "Keep it simple", "You don't really care", "Look around",
                "Don't waste your time", "It could be awesome", "It will be awesome", "It is not so important", "It is wrong", "Only you know what's really important",
                "Know yourself", "Try to relax", "Go out", "The answer is simpler than you might think", "Think about your lifestyle", "Your friends make you rich",
                "Believe in friendship", "Serenity is precious", "Find a solution as soon as possible", "It's not advisable", "It will cost you some extra effort", "You know by yourself", "Sometimes", "Don't waste your time", "You're too involved to understand your situation", "It will forever stay in your heart",
                "It will forever stay in your mind", "It's important", "You'll think about it later", "Things will be better"] 

            for answr_text in answrs:
                logging.info('Adding answr "%s"' % answr_text)
                Answr.add_answr(answr_text)

            Answr.add_answr("Something strange is going on..", 1.0)
            logging.info('Done.')
        else:
            logging.warning('Unauthorized access to /populate')

application = webapp.WSGIApplication([('/populate', PopulatePage)])

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
