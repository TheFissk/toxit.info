# START OF BACK END TEAM MODELS

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
'''
TODO:

- Check ERD for correctness, https://drawsql.app/teams/kyllo-brooks-digital-services/diagrams/reddit-mhs-erd-2 
- Update all classes to ERD spec
- Some classes will need unique pairs or triples
- Test Queries need to be written before testing is done 'test_queries.py' should be created
- Freeze this code and push from gather service into test db using these classes
- Run test queries and iterate

LAST: 
- Docstrings
- Database Wipe
- Prod Migration
- Push Data to prod
- Lock ORM Models

'''

class subreddit(models.Model):
    custom_id = models.CharField(primary_key=True, max_length=20, unique=True,
                                 help_text="Custom key from reddit")
    display_name = models.CharField(max_length=32,
                                    help_text="Display name of the subreddit")

    def __str__(self):
        return self.display_name


class inference_task(models.Model):
    TIME_SCALES = [
        ('hour', 'This Hour'),
        ('day', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('year', 'This Year'),
        ('all', 'All Time')
    ]
    STATUS_TYPES = [
        ("Scheduled"),
        ("In Progress"),
        ("Completed"),
        ("Errored"),
        ("Cancelled")
    ]
    start_sched = models.DateTimeField(help_text='Requested start time')
    # do we want to record when the job actually starts?
    start_time = models.DateTimeField(null=True, blank=True,
                                      help_text='Actual start time')
    time_scale = models.CharField(max_length=5, choices=TIME_SCALES,
                                  help_text="The period overwhich the comments will be harvested")
    min_words = models.IntegerField(default=20, null=True, validators=[MinValueValidator(1), MaxValueValidator(168)],
                                    help_text="The minimum number of words to be considered a valid comment")
    forest_width = models.IntegerField(default=10, validators=[MinValueValidator(0)],
                                       help_text="The number of comments per level to be acquired")
    per_post_n = models.IntegerField(default=1000, validators=[MinValueValidator(1)],
                                     help_text="The maximum number of comments per post to be harvested")
    comments_n = models.IntegerField(default=1000, validators=[MinValueValidator(1)],
                                     help_text="The number of comments to be harvested")
    subreddit_set = models.JSONField(
        help_text="A list of the subreddits to be harvested")
    status = models.CharField(max_length=11, choices=STATUS_TYPES,
                              help_text="The status of the task")

    def __str__(self):
        if (self.start_time):
            return f"Inference job started on: {self.start_time}"
        return f"Inference job scheduled to start on {self.start_sched}"


class subreddit_result(models.Model):
    subreddit = models.ForeignKey(subreddit, on_delete=models.CASCADE,
                                  help_text="The subreddit that was analyzed")
    inference_task = models.ForeignKey(inference_task, on_delete=models.CASCADE,
                                       help_text="The inference task in which this data was collected")
    min_result = models.FloatField(blank=True, null=True,
                                   help_text="The minimum score from this subreddit")
    max_result = models.FloatField(blank=True, null=True,
                                   help_text="The maxmimum score from this subreddit")
    mean_result = models.FloatField(blank=True, null=True,
                                    help_text="The average score from this subreddit")
    std_result = models.FloatField(blank=True, null=True,
                                   help_text="The standard deviation for this subreddit")
    timestamp = models.DateTimeField(
        help_text="The time when the data was collected")
    edges = models.JSONField(help_text="The edges for this subreddit")

    def __str__(self):
        return f"Results for {self.subreddit} collected on {self.inference_task.start_time}"


class subreddit_mod(models.Model):
    username = models.CharField(max_length=32,
                                help_text="The username of the moderator")
    subreddit_result = models.ForeignKey(subreddit_result, on_delete=models.CASCADE,
                                         help_text="The collection that the user was a moderator during")

    def __str__(self):
        return f"User: {self.username}, Subreddit: {self.subreddit_result.subreddit}"


# class comment_author(models.Model):
#     username = models.CharField(max_length=32,)
#     subreddit_result = models.ForeignKey(
#         subreddit_result, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.username


class comment_result(models.Model):
    subreddit_result = models.ForeignKey(
        subreddit_result, on_delete=models.CASCADE)
    subreddit = models.ForeignKey(subreddit, on_delete=models.CASCADE)
    permalink = models.TextField()
    mhs_score = models.FloatField(default=0)
    comment_body = models.TextField()
    comment_author = models.CharField(max_length=32)
    editted = models.BinaryField(default=False)

    def __str__(self):
        return f"Post By: {self.comment_author} in: {self.subreddit}.\nScore: {self.mhs_score}.\nText: {self.comment_body}"


# Not how I would solve this problem
# class Node(models.Model):
#     subreddit_name = models.CharField(max_length=24) # regex = r"^([a-z0-9][_a-z0-9]{2,20})$"\n
#     toxicity_score = models.FloatField(default=0)

#     def __str__(self):
#         return self.subreddit_name


# class Edge(models.Model):
#     start_node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name="start", help_text="Origin of edge")
#     end_node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name="end", help_text="Destination of edge")
#     shared_mod_count = models.PositiveIntegerField(default=0, help_text="Arc weight representing the number of shared moderators between subreddits.")
#     shared_mod_sim = models.FloatField(default=0, help_text="Arc weight representing some magic stats number with a fancy name.")

#     class Meta:
#         unique_together = ('start_node', 'end_node')

#     def validate_unique(self, exclude=None):
#         if self.start_node == self.end_node:
#             raise ValidationError("Node cannot refer to self.")
#         super(Edge, self).validate_unique(exclude=exclude)

#     def __str__(self):
#         return str("from: " + self.start_node.subreddit_name + ", to: " + self.end_node.subreddit_name)
