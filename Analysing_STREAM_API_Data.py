
# coding: utf-8

# In[ ]:


import json
import sys
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from pandas.io.json import json_normalize
from datetime import datetime
import datetime as dt
from IPython.display import display
import matplotlib.pyplot as plt
import plotly.plotly as py
import re


# In[ ]:


file = "2018-02-12.json"



def load_tweets(file):
    with open(file, "r") as f:
        tweets = (json.loads(line) for i, line in enumerate(f.readlines()))
    return tweets

tweets = load_tweets(file)
tweets_data = {"Created At":[], 
               "Username":[],
               "Location":[],
               "Time Zone":[],
               "Tweet": [], 
               "Language":[], 
               "Replies":[],
               "Retweets":[],
               "Favourites":[],
               "Hashtags":[]
              }

for tweet in tweets:
    if "user" in tweet:
        tweets_data["Created At"].append(tweet["created_at"])
        tweets_data["Username"].append(tweet["user"]["screen_name"])
        tweets_data["Location"].append(tweet["user"]["location"])
        tweets_data["Time Zone"].append(tweet["user"]["time_zone"])
        tweets_data["Tweet"].append(tweet["text"])
        tweets_data["Language"].append(tweet["lang"])
        tweets_data["Replies"].append(tweet["reply_count"])
        tweets_data["Retweets"].append(tweet["retweet_count"])
        tweets_data["Favourites"].append(tweet["favorite_count"])
        hashtags=[]
        for hashtag in tweet["entities"]["hashtags"]:
            hashtags.append(hashtag["text"])
        tweets_data["Hashtags"].append(hashtags)
        
    if not "user" in tweet:
        continue

df = pd.DataFrame(tweets_data)   
df["Created At"] = pd.to_datetime(df["Created At"])
df["Created at"] = df["Created At"].dt.time
del df["Created At"]

RT = []
for tweet in df["Tweet"]:
    RT.append(tweet.split()[0]=="RT")
df["RT"] = RT
df = df[["Created at", "Username", "Location", "Language", "Time Zone", "Tweet", "Hashtags", "RT", "Retweets", "Favourites", "Replies"]]
df

#df.to_csv("STREAM_indyref.csv", sep=",")


# In[ ]:


#### STARTING ANALYSIS ###
Hashtag_Counts = {}
for hashtaglist in df["Hashtags"].values:
    for hashtag in hashtaglist:
        if hashtag not in Hashtag_Counts:
            Hashtag_Counts[hashtag] = 1
        else:
            Hashtag_Counts[hashtag] += 1

d = Hashtag_Counts
SortedHashtags = sorted(d.items(), key=lambda x: x[1], reverse=True)

# because text is in tuples within the list, I cannot apply lower function
# so turn tuples into lists within the list, then apply lower
newlist = []
for x in SortedHashtags:
    newnewlist = []
    for y in x:
        y = str(y).lower()
        newnewlist.append(y)
    newlist.append(newnewlist)
display(newlist)


# In[ ]:


df["Language"].value_counts()

df.loc[df["Language"] == "und"]


# In[ ]:


df["RT"].value_counts()


# In[ ]:


df["Time Zone"].value_counts().nlargest(10)


# In[ ]:


dfU = df["Username"].value_counts().nlargest(10)
display(dfU)


# In[ ]:


dfloc = df["Location"].value_counts().nlargest(10)
display(dfloc)


# In[ ]:


import datetime
import math 
df_time = df["Created at"]
df_time = df_time.apply(lambda dt: datetime.time(dt.hour,15*(math.floor(dt.minute/15))))
display(df_time)
df_time.value_counts()

