
# coding: utf-8

# In[3]:


import json
import time
from rauth import OAuth1Service
from auth import TwitterAuth
import os
import urllib.parse
from datetime import datetime
from datetime import timedelta

twitter = OAuth1Service(
    consumer_key = TwitterAuth.consumer_key,
    consumer_secret = TwitterAuth.consumer_secret,
    request_token_url = 'https://api.twitter.com/oauth/request_token',
    access_token_url = 'https://api.twitter.com/oauth/access_token',
    authorize_url = 'https://api.twitter.com/oauth/authorize',
    base_url = 'https://api.twitter.com/1.1/')
session = twitter.get_session(token=[TwitterAuth.access_token,TwitterAuth.access_token_secret])


# In[5]:


outputDir="output_{0}/".format(time.time())
os.mkdir(outputDir)
queries = ["indyref","indyref2","scotref","scottish independence"]

for query in queries:
    minid=None
    page=1
    while True:
        print("Fetching page {} for query {}".format(page,query))
    
        if minid==None:
            params = {"count":100,"q":query,"result_type":"recent"}
            result=session.get("search/tweets.json",params=params)
        else:
            params = {"count":100,"q":query,"result_type":"recent","max_id":minid-1}
            result=session.get("search/tweets.json",params=params)    
            
        result = result.text
    
        fh=open("{0}/{1}_{2}.json".format(outputDir,query,page),"w")
        fh.write(result)
        fh.close()

        result=json.loads(result)

        fh=open("{}/{}_{}_pretty.json".format(outputDir,query,page),"w")
        json.dump(result,fh,indent=4)
        fh.close()
    
        if "statuses" in result and len(result["statuses"])>0:
            print("There are {} results.".format(len(result["statuses"])))
            for status in result["statuses"]:
                if minid==None or status["id"]<minid:
                    minid=status["id"]
            page+=1
            print("To get another page of tweets, max_id should be set to {}".format(minid))
        else:
            minid=None
            break

        time.sleep(5)   

print("DONE! Completed Successfully")

