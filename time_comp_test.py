import praw
import json
import numpy as np
import requests
import time

# imports the classes.py file from this repo
from classes import Sub

# fetch the secrets from the keyfile
keysJSON = open('keys.json')
open_file = keysJSON.read()
model_attribs = json.loads(open_file)['model']
keys = json.loads(open_file)['reddit']
keysJSON.close()

# setup api connection variables
api_key = model_attribs['apikey']
api_url = "https://kyllobrooks.com/api/mhs"

# fetch and construct praw object
reddit = praw.Reddit(
    client_id = keys['client_id'],
    client_secret = keys['client_secret'],
    password = keys['password'],
    user_agent="web:mhs-crawler-bot:v1 (by /u/mhs-crawler-bot)",
    username="mhs-crawler-bot",
)

# set readonly mode
reddit.read_only = False

SUBS_N = 100

# make some empty lists
subs = []

for subreddit in reddit.subreddits.popular(limit=SUBS_N):
    subs.append(subreddit.display_name)

start = time.time()

for sub in subs[:SUBS_N]:
    sample = Sub(sub, api_url, api_key, reddit, scope='week', min_words=20, inference=True, forest_width=10, per_post_n=100, comments_n=500, chunk_size=100)
    print(sample.stats)
    # code here to push data to a dataframe or straight to a database

end = time.time()
rtt = end-start
print('Total Test Time '+str(rtt)+' seconds over '+str(SUBS_N)+' subreddits = mean '+str((rtt/SUBS_N)))
print("scope='week', min_words=20, inference=True, forest_width=10, per_post_n=100, comments_n=500, chunk_size=100")