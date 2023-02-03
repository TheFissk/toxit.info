from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
'''
DONE:
- Check ERD for correctness, https://drawsql.app/teams/kyllo-brooks-digital-services/diagrams/reddit-mhs-erd-2
- Update all classes to ERD spec
- Test migrations (PASSED in SqLite)
- Queries to push to the database should serve as adequate testing
- Freeze this code and push from gather service into test db using these classes
TODO:
- Run test queries and iterate

LAST: 
- Docstrings
- Database Wipe
- Prod Migration
- Push Data to prod
- Lock ORM Models
'''

class Subreddit(models.Model):
    custom_id = models.CharField(primary_key=True, max_length=20, unique=True,
                                    help_text="Custom key from reddit")
    display_name = models.CharField(max_length=32,
                                    help_text="Display name of the subreddit")

    def __str__(self):
        return self.display_name


class Inference_task(models.Model):
    TIME_SCALES =   [
                    ('hour', 'This Hour'),
                    ('day', 'Today'),
                    ('week', 'This Week'),
                    ('month', 'This Month'),
                    ('year', 'This Year'),
                    ('all', 'All Time')
                    ]
    STATUS_TYPES = [
                    ('0', 'Scheduled'),
                    ('1', 'In Progress'),
                    ('2', 'Completed'),
                    ('3', 'Error'),
                    ('4', 'Cancelled')
                    ]
    start_sched = models.DateTimeField(help_text='Requested start time')
    
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
                                    help_text="A set of the subreddits to be harvested")
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES,
                                    help_text="The status of the task")

    def __str__(self):
        if (self.start_sched):
            return f"Inference job scheduled: {self.start_sched}"
 

class Subreddit_result(models.Model):
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE,
                                    help_text="The subreddit that was analyzed")
    inference_task = models.ForeignKey(Inference_task, on_delete=models.CASCADE,
                                    help_text="The inference task in which this data was collected")
    min_result = models.FloatField(blank=True, null=True,
                                    help_text="The minimum score from this subreddit")
    max_result = models.FloatField(blank=True, null=True,
                                    help_text="The maxmimum score from this subreddit")
    mean_result = models.FloatField(blank=True, null=True,
                                    help_text="The average score from this subreddit")
    std_result = models.FloatField(blank=True, null=True,
                                    help_text="The standard deviation for this subreddit")
    timestamp = models.DateTimeField(auto_now_add=True,
                                    help_text="The time when the data was collected")
    edges = models.JSONField(help_text="The edges for this subreddit")

    def __str__(self):
        return f"Results for {self.subreddit} collected on {self.inference_task.start_time}"


class Subreddit_mod(models.Model):
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    subreddit_result = models.ForeignKey(Subreddit_result, on_delete=models.CASCADE,
                                    help_text="The collection that the user was a moderator during")
    username = models.CharField(max_length=32,
                                    help_text="The username of the moderator")
    def __str__(self):
        return f"User: {self.username}, Subreddit: {self.subreddit_result.subreddit}"


class Comment_result(models.Model):
    subreddit_result = models.ForeignKey(Subreddit_result, on_delete=models.CASCADE)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    permalink = models.TextField(help_text='The permalink to the comment sample')
    mhs_score = models.FloatField(default=0, help_text='The mhs inference score of the sample')
    comment_body = models.TextField(help_text='The comment sample')
    username = models.CharField(max_length=32, help_text='The username of the commentor')

    def __str__(self):
        return f"Post By: {self.username} in: {self.subreddit.display_name}.\nScore: {self.mhs_score}.\nText: {self.comment_body}"