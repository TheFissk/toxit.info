import praw
import json
import numpy as np
import requests
from tqdm import tqdm
import datetime
import re


# TODO: Need a class or function for the object describing the matrix of relationships between subs, maybe a sparse matrix
# TODO: Need a class or function to handle pushing the data into a database


class Sub:
    """
    Class object representing a subreddit

    Keyword arguments:
    display_name -- str - required, the display name of the subreddit
    url -- str - required, the url of the api endpoint for inference
    apikey -- str - required, the aipkey for the endpoint
    praw_object -- object - required, the praw reddit object
    scope -- str - defaults to 'week', sets the scope of collection ['hour', 'day', 'week', 'month', 'year', 'all']
    min_words -- int - defaults to 20, the minimum words to collect as a comment
    inference -- bool - defaults to True, build with inference or not
    forest_width -- int - defaults to 10, the number of 'more comments' to traverse in the comment forest
    per_post_n -- int - default to 100, the max number of comments to gather from a single post
    comments_n -- int - defaults to 1000, the max number of comments in total to gather
    chunk_size -- int - defaults to 100, the number of samples to infer in each request to the api

    """
    # defines a constructor
    def __init__(self, display_name, url, apikey, praw_object, scope='week', min_words=20, inference=True, forest_width=10, per_post_n=100, comments_n=1000, chunk_size=100):
        # private parameter members
        self.__scope = scope
        self.__min_words = min_words
        self.__name = display_name
        self.__url = url
        self.__apikey = apikey
        self.__forest_width = forest_width
        self.__per_post_n = per_post_n
        self.__comments_n = comments_n
        self.__chunksize = chunk_size
        # private 
        # TODO: add display_name, date, sub_url, sub_id, logo_url to an __info dict member      
        self.__date = datetime.datetime.now()
        self.__sub = praw_object.subreddit(display_name)
        self.__posts = self.__sub.top(time_filter=self.__scope, limit=None)
        self.__stats = {}
        self.__mods_list = []
        self.__author_list = []
        self.__comment_list = []
        self.__mod_set = {}
        self.__author_set = {}        
        self.__sample_list = []        
        self.__nested_results_list = []   
        self.__results = []      
        # constructors and sanitizers
        self.__fetch_mods()
        self.__fetch_content()
        self.__build_lists()
        self.__build_sets()
        if inference == True:          
            self.__get_mhs_ratings(self.__chunksize)
            self.__results = self.__flatten_results(self.__nested_results_list)
            self.__results = list(self.__results)
            self.__build_stats()

    # constructor function to build moderator list
    def __fetch_mods(self):
        for mod in self.__sub.moderator():
            self.__mods_list.append(mod.name)

    # constructor function to build comments list
    def __fetch_content(self):
        t = tqdm(total=self.__comments_n, desc='Collection: '+ self.__name)
        post_tick = 0
        for post in self.__posts:      
            post.comments.replace_more(limit=self.__forest_width)
            comments = post.comments.list()
            comment_tick = 0
            for comment in comments:
                if comment_tick >= self.__per_post_n: 
                    break
                if comment.author is not None and self.__count_words(comment.body) > self.__min_words:
                    t.update(1)
                    data = {
                        'body': self.__sanitize(comment.body),
                        'author': comment.author.name,
                        'permalink': comment.permalink
                        # TODO: add more data to collect here and test the collection time difference, if it is low then collect more
                    }
                    self.__comment_list.append(data)
                    if len(self.__comment_list) == self.__comments_n:
                        break
                    comment_tick += 1
                    #print('post :' + str(post_tick) + ' comment tick :' + str(comment_tick))
            if len(self.__comment_list) == self.__comments_n:
                break
            post_tick += 1

    # defines a function to build lists from a dict
    def __build_lists(self):
        for data in self.__comment_list:
            self.__sample_list.append(data['body'])
            self.__author_list.append(data['author'])


    # defines a funtion to clean text in the strings from weird chars
    def __sanitize(self, item):
        item = item.strip()
        item = item.strip('\n')
        item = item.replace('\n','')
        item = item.replace('\n\n','')
        item = item.replace('\\','')
        item = item.replace('/','')
        return item
   
    # defines a funtion to perform inference on the chunks
    def __request_inferance(self, instances, apikey, url):
        payload = { "instances": instances }
        headers = {'apikey':  apikey}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        jsonresp = response.json()
        return jsonresp

    # defines a helper function to chunk the comments for serving to inference
    def __chunker(self, iterable, chunksize):
        return zip(*[iter(iterable)] * chunksize)

    # defines a helper function to flatten the results
    def __flatten_results(self, predictions):
        for item in predictions:
            try:
                yield from self.__flatten_results(item)
            except TypeError:
                yield item

    # defines a function that carries out inference on chunks of N samples
    def __get_mhs_ratings(self, N):
        for chunk in tqdm (self.__chunker(self.__sample_list, N), total= len(self.__sample_list)/self.__chunksize, desc='Inference: '+ self.__name):
            while True:
                try:
                    response = self.__request_inferance(chunk, self.__apikey, self.__url)
                    self.__nested_results_list.append(response['predictions'])
                except requests.exceptions.HTTPError as e:
                    # could add a logging call here for the error 'e'
                    continue
                break
            pass
    
    # defines a funtion to count words
    def __count_words(self, sentence):
        return len(re.findall(r'\w+', sentence))

    # defines a function to build unordered sets from author and mod list members
    def __build_sets(self):
        self.__mod_set = set(self.__mods_list)
        self.__author_set = set(self.__author_list)

    # builds an array of descriptive statistics for the results
    def __build_stats(self):
        arr = np.array(self.__results)
        self.stats = {
            'min': arr.min(),
            'max': arr.max(),
            'mean': arr.mean(),
            'std': arr.std()
        }

    # defines a convenience function to run inference after the object already exists or if it was created with inference=False
    def infer(self):
        """Convenience method to carry out inference on the Sub after it has been constructed with inference=False"""
        self.__get_mhs_ratings(self.__chunksize)
        self.__results = self.__flatten_results(self.__nested_results_list)
        self.__results = list(self.__results)
        self.__build_stats()

    # Access functions
    def name(self):
        """Returns the display name of the subreddit"""
        return self.__name

    def date(self):
        """Returns the date of sample gathering"""
        return self.__date
    
    def mods(self):
        """Returns the list of moderators"""
        return self.__mods_list

    def samples(self):
        """Returns the list of text samples gathered"""
        return self.__sample_list

    def authors(self):
        """Returns the list of comment authors"""
        return self.__author_list

    def results(self):
        """Returns a list of inference results"""
        return self.__results
    
    def stats(self):
        """Returns a dict of descriptive stats: [min, max, mean, std]"""
        return self.__stats
    
    def author_set(self):
        """Returns a python set of authors"""
        return self.__author_set

    def mod_set(self):
        """Returns a python set of moderators"""
        return self.__mod_set