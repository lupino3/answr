import logging
import tweepy
from models import ApplicationData, Answr, Question
from utils import detect_language_from_msg

logging.info('Running the answr twitterbot!')

# 1. Login
(ctoken, csecret, key, secret) = ApplicationData.getTwitterAuth()

auth = tweepy.OAuthHandler(ctoken, csecret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)
logging.info('Login done!')

followers = api.followers()
friends = api.friends()
logging.info('I have %d followers and I follow %d people!' % (len(followers), len(friends)))

# 2. Auto-follow people who follow me
to_follow = [x for x in followers if x not in friends]
logging.info('Must follow back %d people!' % len(to_follow))
for user in to_follow:
    try:
        user.follow()
    except tweepy.TweepError, e:
        logging.warning(e)

# 2. Reading last messages sent to me
last_id = ApplicationData.getLastAnswredTweetId()
if not last_id:
    logging.info('First time that I answer!')
    mentions = api.mentions(count = 200)
else:
    logging.info('Last ID: %d' % last_id)
    mentions = api.mentions(count = 200, since_id = last_id)

logging.info("Got %d mentions to answr!" % len(mentions))

# 3. Random answrs for everybody!
for status in mentions:
    try:
        question = " ".join([x for x in status.text.split() if not x.startswith('@')])
        lang, confidence = detect_language_from_msg(question)
    except:
        logging.warning("Error during language detection. Switching back to en")
        lang = "en"

    answr = Answr.answr(lang).text
    Question.save(status.text, answr, 'twitter', "@%s" % status.author.screen_name, lang)
    api.update_status("@%s %s" % (status.author.screen_name, answr), status.id)
    logging.info("I replied to @%s (%s) with %s, is that ok?" % (status.author.screen_name, status.text, answr))

    # I don't know the order of the IDs, so I have to check every time
    if status.id > last_id:
        last_id = status.id

# 4. Save the last ID
if last_id:
    ApplicationData.setLastAnswredTweetId(last_id)
