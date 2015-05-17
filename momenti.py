from google.appengine.api import urlfetch
import logging

url = "http://www.momentizen.it/webtest/drupalMZ/cron.php?cron_key=WaV3XbjMV1hvNtCSD4_Mq0AxJ1cYnM5qgxBKeG7gJH4"
result = urlfetch.fetch(url)

logging.info("Request done. Error code: %s", result.status_code)
