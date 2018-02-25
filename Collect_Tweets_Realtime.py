
# coding: utf-8

# In[ ]:


class TwitterAuth:
    consumer_key=""
    consumer_secret=""
    access_token=""
    access_token_secret=""


# In[ ]:


import json
import time
from rauth import OAuth1Service
from auth import TwitterAuth
import os
import urllib.parse
import os
from datetime import datetime
from datetime import timedelta

twitter = OAuth1Service(
    consumer_key=TwitterAuth.consumer_key,
    consumer_secret=TwitterAuth.consumer_secret,
    request_token_url = 'https://api.twitter.com/oauth/request_token',
    access_token_url = 'https://api.twitter.com/oauth/access_token',
    authorize_url = 'https://api.twitter.com/oauth/authorize',
    base_url = 'https://api.twitter.com/1.1/')
session = twitter.get_session(token=[TwitterAuth.access_token,TwitterAuth.access_token_secret])


# In[ ]:


outputDir = "output_streaming_sum_Tweets_48_hours"
try:
    os.mkdir(outputDir)
except OSError as error:
    if error.errno==17:
        pass
    else:
        raise error

terms=["indyref","indyref2","scotref","scottish independence", "scottish referendum", "scotland referendum"]
print("{} - Starting stream to track {} ".format(datetime.now(),terms))
r = session.post("https://stream.twitter.com/1.1/statuses/filter.json",data={"track":terms},stream=True)
print("{} - Stream started. ".format(datetime.now()))

d=datetime.today()
fh=open("{}/{}-{:02d}-{:02d}.json".format(outputDir,d.year,d.month,d.day),"ab")
line_count=0

today = datetime.now() 
in_48_hours = today + timedelta(days=2)

for line in r.iter_lines():
    if line:
        fh.write(line)
        fh.write(b'\n')
        line_count+=1
        if datetime.now() > in_48_hours:
            print("{} - Have collected tweets for 48 hours. Stopping tweet collection now...".format(datetime.now()))
            break
    time.sleep(5)
    
fh.close()
r.close()

