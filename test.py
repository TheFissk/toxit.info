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


# TODO: Actually build one function per class that tests the class 


# demonstrate the set similarity measure function above
A = time.time()

s = time.time()
sampleA = Sub('AskReddit', api_url, api_key, reddit, scope='week', 
                                                min_words=20, 
                                                inference=False, 
                                                forest_width=10, 
                                                per_post_n=100, 
                                                comments_n=500, 
                                                chunk_size=100
                                            )
sampleB = Sub('ukraine', api_url, api_key, reddit, scope='week', 
                                                min_words=20, 
                                                inference=False, 
                                                forest_width=10, 
                                                per_post_n=100, 
                                                comments_n=500, 
                                                chunk_size=100
                                            )
e = time.time()
print('Fetch Time: '+str((e-s)/2))
print ('sampleA - Author Set Cardinality: '+str(len(sampleA.author_set())))
print ('sampleA - Author List Length: '+str(len(sampleA.authors())))
print ('sampleB - Author Set Cardinality: '+str(len(sampleB.author_set())))
print ('sampleB - Author List Length: '+str(len(sampleB.authors())))
print ('sampleA - Sample List Length: '+str(len(sampleA.samples())))
print ('sampleB - Sample List Length: '+str(len(sampleB.samples())))
s = time.time()
sampleA.infer()
sampleB.infer()
e = time.time()
print('Inference Time: '+str((e-s)/2))
print('sampleA - Results List Length: '+str(len(sampleA.results())))
print ('sampleB - Results List Length: '+str(len(sampleB.results())))
s = time.time()
setA = sampleA.author_set()
setB = sampleB.author_set()
print ('Jaccard Similarity: '+ str(jaccard_index(setA, setB)))
e = time.time()
print('Jaccard Time: '+str(e-s))
print('Sample A Collection Date :'+ str(sampleA.date()))
print(sampleA.stats)
print('Sample B Collection Date :'+ str(sampleB.date()))
print(sampleB.stats)

B = time.time()

print('RTT : '+str((B-A)/2))