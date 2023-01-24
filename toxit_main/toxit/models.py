from django.db import models


class Snapshot(models.Model):
    """
        snapshot_name\n
            optional name value for the snapshot. In the future autopopulating with snapshot date would be cool.\n

        snapshot_date:\n
            The date and time of when the snapshot was gathered and created\n

        node_table:\n
            the collection of all nodes or subreddits caputed in the snapshot\n

        edge_table\n
            all of the connecting edges or arcs between all subreddits stored in node_table\n 
    """
    snapshot_name = models.CharField(max_length=128, blank=True, null=True, help_text="optional way to name the snapshot")
    snapshot_date = models.DateTimeField('Date & Time snapshot was collected', primary_key=True, help_text="When snapshot was captured.") # maybe this should be PK
    node_table = models.ForeignKey('Node', blank=True, null=True, on_delete=models.SET_NULL, related_name="nodes", help_text="All subreddit nodes related to the snapshot.")
    edge_table = models.ForeignKey('Node', blank=True, null=True, on_delete=models.SET_NULL, related_name="edges", help_text="All connections between nodes in the snapshot.")

    # does not behave as expected
    # def __str__(self):
    #     return self.snapshot_date

class Node(models.Model):
    """
        sub_name:\n
            subreddits are 3 to 21 chars, letters numbers or '_', only '_' not 1st char;\n
                -->     regex = r"^([a-z0-9][_a-z0-9]{2,20})$"\n

        toxicity_score:\n
            float that indicates how toxic the subreddit is from -1.0 to 1.0\n
                -->     -1.0 = most toxic; 1.0 = most wholesome \n

        score_tree: (to be implemented)\n
            - stores a root for a tree holding all post + comments\n
            - illustrates how the toxicity_score was calculated\n
    """
    sub_name = models.CharField(max_length=24, primary_key=True, help_text="the name of the subreddit scored by the A.I. retrieved by the web crawler.")
    toxicity_score = models.FloatField(default=0, help_text="Indicator of how toxic the Subreddit is ranging from -1.0 to 1.0; where -1.0 is the most toxic and 1.0 is the most wholesome.")
    # score_summary = models.ForeignKey('ScoreTree', on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_name


class Edge(models.Model):
    """
        start_node:\n
            Stored reference (Foreign key) of node where edge originates\n

        end_node:\n
            Stored reference (Foreign key) of node where edge terminates\n

        shared_mod_count\n
            Integer value of the number, >= 0, of moderators shared between the two subreddits\n

        shared_mod_sim (to be implemented)\n
            I dont really get what this is outside of a float... maybe it isnt even stored as a float lol\n
    """
    start_node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name="start", help_text="Origin of edge")
    end_node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name="end", help_text="Destination of edge")
    shared_mod_count = models.PositiveIntegerField(default=0, help_text="Arc weight representing the number of shared moderators between subreddits.")
    shared_mod_sim = models.FloatField(default=0, help_text="Arc weight representing some magic stats number with a fancy name.")
    # shared_commenters
    # shared_commenters


"""
    Below is a rough outline of the other classes I believe are necessary to store
    all the relevant data related to our graph and whatever is needed to show how
    we came to the conclusions we did. They are not necessary however to try and
    get visjs up and running on a django web app.

    score tree
    Used to hold all the relavent breakdown information we need to 
    show off the posts and comments in a subreddit node view reviewed with the AI
    with the scoring the AI assigned to what text. Score tree would just be a 
    reference to all the Post and Comment entries

    Post 
    just the relevant info: score, text, poster name

    comment 
    just the relevant info: score, text, commenter name
    might need some info on if it is a parent or child comment
    perhaps the post can be the parent of root comments
"""   
# class ScoreTree:
#     # is a root field and leaf field needed ?
#     sub_name = models.CharField(max_length=24, primary_key=True) # maybe this is dumb?
#     post = models.ForeignKey('Post', on_delete=models.CASCADE) # cascade might not be necessary?

# class Post:
#     post_score = models.FloatField(default=0)
#     post_text = models.CharField(max_length=300)
#     poster_username = models.CharField(max_length=300) # should match reddit naming limitations
#     comment = models.ForeignKey('Comment', on_delete=models.CASCADE)

# class Comment:
#     comment_score = models.FloatField(default=0)
#     comment_text = models.CharField(max_length=300)
#     commenter_username = models.CharField(max_length=300) # should match reddit naming limitations
#     comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)