from django.utils import simplejson as json
from google.appengine.api import urlfetch
import urllib

def detect_language_from_msg(msg):
    url = "http://www.google.com/uds/GlangDetect?%s" % urllib.urlencode({'v' : '1.0', 'q' : msg.encode('utf-8')})
    result = urlfetch.fetch(url)
    data = json.loads(result.content)["responseData"]
    return data["language"], float(data["confidence"])

