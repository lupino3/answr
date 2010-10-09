import logging
import tweepy
from models import ApplicationData, Answr

logging.info('Running the answr twitterbot!')

# 1. Login
auth = tweepy.BasicAuthHandler("answrit", "***")
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

# 2. Lettura degli ultimi messaggi diretti a me
last_id = ApplicationData.getLastAnswredTweetId()
if not last_id:
    logging.info('First time that I answer!')
    mentions = api.mentions(count = 200)
else:
    logging.info('Last ID: %d' % last_id)
    mentions = api.mentions(count = 200, since_id = last_id)

logging.info("Got %d mentions to answr!" % len(mentions))

# 3. Risposta in maniera casuale a tutti 
for status in mentions:
    answr = Answr.get_random()
    api.update_status("@%s %s" % (status.author.screen_name, answr.text), status.id)
    logging.info("I replied to @%s (%s) with %s, is that ok?" % (status.author.screen_name, status.text, answr.text))

    # Non so in che ordine mi sono tornati gli status..
    if status.id > last_id:
        last_id = status.id

# 4. Salvataggio ultimo ID
if last_id:
    ApplicationData.setLastAnswredTweetId(last_id)
