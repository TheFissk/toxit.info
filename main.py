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

def jaccard_index(A, B):
    """A function that returns the Jaccard similarity index for a given two sets:  
    
    |AnB| / |AuB|
    
    A -- set - required, a python set object
    B -- set - required, a python set object
    """
    return len( A.intersection(B) ) / len( A.union(B) )

# demonstrate the set similarity measure function above

s = time.time()
sampleA = Sub('AskReddit', api_url, api_key, reddit, inference=False, comments_n=1000, forest_width=1, per_post_n=1000)
sampleB = Sub('AmItheAsshole', api_url, api_key, reddit, inference=False, comments_n=1000, forest_width=1, per_post_n=1000)
e = time.time()
print('Fetch Time: '+str(e-s))
print ('sampleA - Author Set Cardinality: '+str(len(sampleA.author_set())))
print ('sample A - Author List Length: '+str(len(sampleA.authors())))
print ('sampleB - Author Set Cardinality: '+str(len(sampleB.author_set())))
print ('sampleB - Author List Length: '+str(len(sampleB.authors())))
s = time.time()
setA = sampleA.author_set()
setB = sampleB.author_set()
print ('Jaccard Similarity: '+ str(jaccard_index(setA, setB)))
e = time.time()
print('Jaccard Time: '+str(e-s))