
# coding: utf-8

# In[ ]:


import json
import numpy as np
import datetime as dt
import os
import pandas as pd
from pandas import Series, DataFrame
from IPython.display import display
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import re


# In[ ]:


import glob
inputDir="output"

bdata = {      "Created At":[], 
               "Username":[],
               "Location":[],
               "Time Zone":[],
               "Tweet": [], 
               "Language":[], 
               "Retweets":[],
               "Favourites":[],
               "Hashtags":[]
          }

for file in glob.glob("{0}/*.json".format(inputDir)):
    fh=open(file,"r")
    tweets = json.load(fh)
    for tweet in tweets["statuses"]:
            if "user" in tweet:
                bdata["Created At"].append(tweet["created_at"])
                bdata["Time Zone"].append(tweet["user"]["time_zone"])
                bdata["Username"].append(tweet["user"]["screen_name"])
                bdata["Location"].append(tweet["user"]["location"])
                bdata["Tweet"].append(tweet["text"])
                bdata["Language"].append(tweet["lang"])
                bdata["Retweets"].append(tweet["retweet_count"])
                bdata["Favourites"].append(tweet["favorite_count"])
                hashtags=[]
                for hashtag in tweet["entities"]["hashtags"]:
                    hashtags.append(hashtag["text"])
                bdata["Hashtags"].append(hashtags)
        
df1 = pd.DataFrame(bdata) 
df1["Created At"] = pd.to_datetime(df1["Created At"])
RT = []
for tweet in df1["Tweet"]:
    RT.append(tweet.split()[0]=="RT")
df1["RT"] = RT
df1 = df1[["Created At", "Username", "Location","Time Zone", "Tweet", "Hashtags", "RT", "Retweets", "Favourites"]]                        
# df1.sort_values("Created At", ascending=True, inplace=True)
df1

# df1.to_csv("REST_indyref.csv", sep=",")


# In[ ]:


Hashtag_Counts = {}
for hashtaglist in df1["Hashtags"].values:
    for hashtag in hashtaglist:
        if hashtag not in Hashtag_Counts:
            Hashtag_Counts[hashtag] = 1
        else:
            Hashtag_Counts[hashtag] += 1

d1 = Hashtag_Counts
SortedHashtags1 = sorted(d1.items(), key=lambda x: x[1], reverse=True)
SortedHashtags1
# because text is in tuples within the list, I cannot apply lower function
# so turn tuples into lists within the list, then apply lower
# newlist1 = []
# for x in SortedHashtags1:
#     newnewlist1 = []
#     for y in x:
#         y = str(y).lower()
#         newnewlist1.append(y)
#     newlist1.append(newnewlist1)
# display(newlist1)


# In[ ]:


df1["Time Zone"].value_counts().nlargest(30)


# In[ ]:


df1["Username"].value_counts().nlargest(10)

dfbot = df1[(df1["Username"] == "IsThisAB0t")]
# dfbot["RT"].value_counts().max()
dfbot["Retweets"].value_counts().max()
# dfbot


# In[ ]:


df1["RT"].value_counts()


# In[ ]:


df2 = df1["Location"]
df2.value_counts().nlargest(10)
mapper = {
    "Scotland":"Scotland, United Kingdom",
    "Glasgow":"Glasgow, United Kingdom",
    "Glasgow, Scotland":"Glasgow, United Kingdom",
    "London, England":"London, United Kingdom",
    "Edinburgh":"Edinburgh, United Kingdom",
    "Edinburgh, Scotland":"Edinburgh, United Kingdom"
}

df2["Location_"] = df2.map(mapper)
df2["Location_"].value_counts()


# In[ ]:


df3 = df1["Time Zone"]
df3.value_counts().nlargest(10)
# mapper = {
#     "Scotland":"Scotland, United Kingdom",
#     "Glasgow":"Glasgow, United Kingdom",
#     "Glasgow, Scotland":"Glasgow, United Kingdom",
#     "London, England":"London, United Kingdom",
#     "Edinburgh":"Edinburgh, United Kingdom",
#     "Edinburgh, Scotland":"Edinburgh, United Kingdom"
# }

# df2["Location_"] = df2.map(mapper)
# df2["Location_"].value_counts().nlargest(10)


# In[ ]:


import datetime
df_day = df1["Created At"]
df_day = df_day.apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day))
df_day.value_counts().nlargest(10)

