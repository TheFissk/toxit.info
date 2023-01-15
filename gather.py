import praw
import json
import numpy as np
import requests

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


# # fill the list with the top subreddits in descending order of subscriber numbers
# subs = []
# for subreddit in reddit.subreddits.popular(limit=None):
#     subs.append(subreddit.display_name)

# define a class that has a method in its constructor to build ordered lists of mods, comments, and commentors
class Sub:
    """
    Class object representing a subreddit

    Keyword arguments:
    display_name -- str - required, the display name of the subreddit
    url -- str - required, the url of the api endpoint for inference
    apikey -- str - required, the aipkey for the endpoint
    praw_object -- object - required, the praw reddit object
    inference -- bool - defaults to True, build with inference or not
    forest_width -- int - defaults to 10, the number of 'more comments' to traverse in the comment forest
    per_post_n -- int - default to 100, the max number of comments to gather from a single post
    comments_n -- int - defaults to 1000, the max number of comments in total to gather
    chunk_size -- int - defaults to 50, the number of samples to infer in each request to the api

    """
    # defines a constructor
    def __init__(self, display_name, url, apikey, praw_object, inference=True, forest_width=10, per_post_n=100, comments_n=1000, chunk_size=50):
        # public members
        self.name = display_name
        self.mhs_rating = 0.0
        # private members
        self.__mods_list = []
        self.__sub = praw_object.subreddit(display_name)
        self.__posts = self.__sub.top(time_filter="week", limit=None)
        self.__url = url
        self.__apikey = apikey
        self.__forest_width = forest_width
        self.__per_post_n = per_post_n
        self.__comments_n = comments_n
        self.__chunksize = chunk_size
        self.__sample_list = []
        self.__author_list = []
        self.__results_list = []
        self.__stats = [0,0,0,0]
        self.__mod_set = {}
        self.__author_set = {}
        # constructors and sanitizers
        self.__build_mods()
        self.__build_content()
        self.__sanitize()
        self.__build_sets()
        if inference == True:          
            self.__get_mhs_ratings(self.__chunksize)
            self.__build_stats()

    # constructor function to build moderator list
    def __build_mods(self):
        for mod in self.__sub.moderator():
            self.__mods_list.append(mod.name)

    # constructor function to build comments list
    def __build_content(self):
        for post in self.__posts:
            post_comment_count = 0
            post.comments.replace_more(limit=self.__forest_width)
            for comment in post.comments.list():
                try:
                    post_comment_count += 1
                    self.__sample_list.append(comment.body)
                except AttributeError:
                    self.__sample_list.append('NULL')
                try:
                    self.__author_list.append(comment.author.name)
                except AttributeError:
                    self.__author_list.append('NULL')
                if len(self.__sample_list) >= self.__comments_n or post_comment_count >= self.__per_post_n:
                    break
                else:
                    continue
            if len(self.__sample_list) >= self.__comments_n:
                break
            else:
                continue
     
    # defines a funtion to clean text in the strings from weird chars
    def __sanitize(self):
        self.__sample_list[:] = [item for item in self.__sample_list if item.strip() == item]
        self.__sample_list[:] = [item for item in self.__sample_list if item.strip('\n') == item]
        self.__sample_list[:] = [item for item in self.__sample_list if item.replace('\n','') == item]
        self.__sample_list[:] = [item for item in self.__sample_list if item.replace('\n\n','') == item]
        self.__sample_list[:] = [item for item in self.__sample_list if item.replace('\\','') == item]
        self.__sample_list[:] = [item for item in self.__sample_list if item.replace('/','') == item]
    
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
    def __flatten(self, predictions):
        for item in predictions:
            try:
                yield from self.__flatten(item)
            except TypeError:
                yield item

    # defines a function that carries out inference on chunks of N samples
    def __get_mhs_ratings(self, N):
        for chunk in self.__chunker(self.__sample_list, N):
            while True:
                try:
                    response = self.__request_inferance(chunk, self.__apikey, self.__url)
                    self.__results_list.append(response['predictions'])
                except requests.exceptions.HTTPError as e:
                    # could add a logging call here for the error 'e'
                    continue
                break
        return list(self.__flatten(self.__results_list))

    # defines a function to build unordered sets from author and mod list members
    def __build_sets(self):
        self.__mod_set = set(self.__mods_list)
        self.__author_set = set(self.__author_list)

    # builds an array of descriptive statistics for the results
    def __build_stats(self):
        arr = np.array(self.__results_list)
        self.__stats[0] = arr.min()
        self.__stats[1] = arr.max()
        mean = arr.mean()
        self.__stats[2] = mean
        self.mhs_rating = mean
        self.__stats[3] = arr.std()

    # defines a convenience function to run inference after the object already exists or if it was created with inference=False
    def infer(self):
        self.__get_mhs_ratings(self.__chunksize)
        self.__build_stats()

    # Access functions
    def mods(self):
        return self.__mods_list

    def samples(self):
        return self.__sample_list

    def authors(self):
        return self.__author_list
    
    def stats(self):
        return self.__stats
    
    def author_set(self):
        return self.__author_set

    def mod_set(self):
        return self.__mod_set

# example code to build a sub object from the subreddit display name 'cork' i think this is county cork in ireland
cork = Sub('cork', api_url, api_key, reddit, inference=False)

# you can interact with this object with its accessor methids for mods, samples, and author
print(cork.stats())
cork.infer()
print(cork.stats())