import praw
import json
import numpy as np
import requests

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

# example code to build a sub object from the subreddit display name 'cork' i think this is county cork in ireland
cork = Sub('cork', api_url, api_key, reddit, inference=False)

# you can interact with this object with its accessor methids for sets, lists and stats
cork.infer()

# stats are [min, max, mean, std]
print(cork.stats())


