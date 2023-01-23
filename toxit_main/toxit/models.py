from django.db import models


class Node(models.Model):
    """
        sub_name:
            subreddits are 3 to 21 chars, letters numbers or '_', only '_' not 1st char;
                -->     regex = r"^([a-z0-9][_a-z0-9]{2,20})$"

        toxicity_score:
            float that indicates how toxic the subreddit is from -1.0 to 1.0
                -->     -1.0 = most toxic; 1.0 = most wholesome 
    """
    sub_name = models.CharField(max_length=24, primary_key=True, help_text="the name of the subreddit scored by the A.I. retrieved by the web crawler.")
    toxicity_score = models.FloatField(help_text="Indicator of how toxic the Subreddit ranging from -1.0 to 1.0 where -1.0 is the most toxit and 1.0 is the most wholesome.")
    # comments (FK)


# class Edge(models.Model):
    # node_parent           --> node
    # node_child            --> node
    # moderator_simularity  --> float?
    # moderator_count       --> int
    # commenter_simularity
    # commenter_count
    

# class Comment(models.Model):
#     comment_text = models.CharField(max_length=200, help_text="I don't remember how much text the AI stores")