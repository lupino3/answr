from google.appengine.ext import db
import logging
import random

# Not sure if I can put those lists in the Question class
_TECHS = ['web', 'twitter', 'xmpp']

class Question(db.Model):
    """An answrd question."""
    # The question asked
    text = db.StringProperty(required = True)

    # The answr given
    answr = db.StringProperty(required = True)

    # The technology used
    tech = db.StringProperty(choices = _TECHS)

    # An ID of who asked the question (xmpp_id, twitter_username, ip)
    who = db.StringProperty()

    # The language used
    lang = db.StringProperty()

    # When the question was answrd (object creation time)
    when = db.DateTimeProperty(auto_now_add = True)

    @staticmethod
    def save(text, answr, tech = None, who = None, lang = None):
        """Saves data about a question and returns the ID of the saved
        question"""
        q = Question(text = unicode(text, 'utf8'), answr = unicode(answr, 'utf8'), tech = tech, who = who, lang = lang)
        return q.put().id()

class Answr(db.Model):
    """An answr that the magic chick will give to the user"""
    text = db.StringProperty(required = True)

    # A random number between 0 and 1, that will be used during the retrieval
    # phase
    rand = db.FloatProperty(required = True)

    # Language
    lang = db.StringProperty(required = True)

    def to_json(self):
        return '{"text" : "%s"}' % self.text

    @staticmethod
    def answr(lang = "en"):
        """Gets a random answr. The hypothesis is that there is an answr having
        rand = 1, so that the query always returns a value"""
        answr = Answr.gql("WHERE rand >= :1 AND lang = :2 ORDER BY rand ASC LIMIT 1", random.random(), lang).get()
        return answr

    @staticmethod
    def add_answr(answr_text, lang, rand = None):
        if not rand:
            rand = random.random()

        answr_text = unicode(answr_text, 'utf8')
        a = Answr(text = answr_text, lang = lang, rand = rand)
        ApplicationData.incrementAnswrCounter()
        a.put()


class ApplicationData(db.Model):
    name = db.StringProperty()
    value = db.StringProperty()

    @staticmethod
    def getTwitterAuth():
        consumer_token  = db.Query(ApplicationData).filter('name =', 'twitter_oauth_consumer_key').get()
        consumer_secret = db.Query(ApplicationData).filter('name =', 'twitter_oauth_consumer_secret').get()
        key = db.Query(ApplicationData).filter('name =', 'twitter_oauth_key').get()
        secret = db.Query(ApplicationData).filter('name =', 'twitter_oauth_secret').get()

        return (consumer_token.value, consumer_secret.value, key.value, secret.value)

    @staticmethod
    def getAnswrCounter():
        counter = db.Query(ApplicationData).filter('name =', 'answrcounter').get()
        if not counter:
            logging.info('First access to the counter')
            counter = ApplicationData(name = 'answrcounter', value = "0")

        return counter

    @staticmethod
    def incrementAnswrCounter():
        counter = ApplicationData.getAnswrCounter()
        counter.value = str(int(counter.value) + 1)
        counter.put()

    @staticmethod
    def getLastAnswredTweetId():
        id = db.Query(ApplicationData).filter('name =', 'lastansweredtweetid').get()
        if not id:
            logging.info('First answer to tweets')
            return None

        return int(id.value)

    @staticmethod
    def setLastAnswredTweetId(new_id):
        id = db.Query(ApplicationData).filter('name =', 'lastansweredtweetid').get()
        if id is None:
            id = ApplicationData(name = 'lastansweredtweetid', value = "0")

        id.value = str(new_id)
        id.put()
