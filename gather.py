import praw
import time
import json

keysJSON = open('keys.json')
# the reddit at the end filters for just the reddit keys, its not mandatory, you could grab the whole file.
# but this cuts down on the typing
keys = json.loads(keysJSON.read())['reddit']
keysJSON.close()

reddit = praw.Reddit(
    client_id = keys['client_id'],
    client_secret = keys['client_secret'],
    password = keys['password'],
    user_agent="web:mhs-crawler-bot:v1 (by /u/mhs-crawler-bot)",
    username="mhs-crawler-bot",
)

# Define some globals
FOREST_WIDTH = 10
N = 1000
PER_POST_N = 100

# set readonly mode
reddit.read_only = False

# make an empty list of subreddit names
subs = []


# # fill the list with the top subreddits in descending order of subscriber numbers
# for subreddit in reddit.subreddits.popular(limit=None):
#     subs.append(subreddit.display_name)

# define a class that has a method in its constructor to build ordered lists of mods, comments, and commentors
class Sub:
    # defines a constructor
    def __init__(self, display_name):
        self.name = display_name
        self.mhs_rating = 0.0
        self.__mods_list = []
        self.__sub = reddit.subreddit(display_name)
        self.__posts = self.__sub.top(time_filter="week", limit=None)
        self.__sample_list = []
        self.__author_list = []
        self.__build_mods()
        self.__build_content()

    # constructor function to build moderator list
    def __build_mods(self):
        for mod in self.__sub.moderator():
            self.__mods_list.append(mod.name)

    # constructor function to build comments list
    def __build_content(self):
        for post in self.__posts:
            post_comment_count = 0
            post.comments.replace_more(limit=FOREST_WIDTH)
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
                if len(self.__sample_list) >= N or post_comment_count >= PER_POST_N:
                    break
                else:
                    continue
            if len(self.__sample_list) >= N:
                break
            else:
                continue

    # Access functions
    def mods(self):
        return self.__mods_list

    def samples(self):
        return self.__sample_list

    def authors(self):
        return self.__author_list


# example code to build a sub object from the subreddit display name 'cork' i think this is county cork in ireland
cork = Sub('cork')

# you can interact with this object with its accessor methids for mods, samples, and author

cork_samples = cork.samples()

for i in cork_samples:
    print(i)
