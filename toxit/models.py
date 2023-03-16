from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Subreddit(models.Model):
    class Meta:
        db_table = 'toxit_subreddit'
        managed = False
    custom_id = models.CharField(primary_key=True, max_length=20, unique=True,
                                    help_text="Custom key from reddit")
    display_name = models.CharField(max_length=32,
                                    help_text="Display name of the subreddit")

    def __str__(self):
        return self.display_name


class Inference_task(models.Model):
    class Meta:
        db_table = 'toxit_inference_task'
        managed = False

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
                                    help_text="[DEPRECIATED]")
    per_post_n = models.IntegerField(default=1000, validators=[MinValueValidator(1)],
                                    help_text="The maximum number of comments per post to be harvested")
    comments_n = models.IntegerField(default=1000, validators=[MinValueValidator(1)],
                                    help_text="The number of comments to be harvested")
    subreddit_set = models.JSONField(
                                    help_text="A set of the subreddits to be harvested")
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES,
                                    help_text="The status of the task", default=0)
    
    # used by views.py to package data for ajax call 
    def get_subreddits_for_inference_task(self):
        return Subreddit_result.objects.filter(inference_task=self).select_related('subreddit')
    
    def get_mod_edges_for_inference_task(self):
        return Mod_edge.objects.filter(inference_task=self)
    
    def get_author_edges_for_inference_task(self):
        return Author_edge.objects.filter(inference_task=self)
    
    # used by snapshot select to display count of nodes in a snapshot
    def subreddit_count(self):
        return Subreddit_result.objects.filter(inference_task=self).count()

    def __str__(self):
        if (self.start_sched):
            return f"Inference job scheduled: {self.start_sched}"
 

class Subreddit_result(models.Model):
    class Meta:
        db_table = 'toxit_subreddit_result'
        managed = False

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
    edges = models.JSONField(help_text="[DEPRECIATED]")

    def getNodeInfo(self, threshold):
        return  Comment_result.objects.filter(subreddit_result=self, mhs_score__gt=threshold).count()

    def __str__(self):
        return f"Results for {self.subreddit} collected on {self.inference_task.start_sched}"


class Subreddit_mod(models.Model):
    class Meta:
        db_table = 'toxit_subreddit_mod'
        managed = False

    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    subreddit_result = models.ForeignKey(Subreddit_result, on_delete=models.CASCADE,
                                    help_text="The subreddit the user was a moderator for, in a specific result")
    username = models.CharField(max_length=32,
                                    help_text="The username of the moderator")
    def __str__(self):
        return f"User: {self.username}, Subreddit: {self.subreddit_result.subreddit}"


class Comment_result(models.Model):
    class Meta:
        db_table = 'toxit_comment_result'
        managed = False

    subreddit_result = models.ForeignKey(Subreddit_result, on_delete=models.CASCADE)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    permalink = models.TextField(help_text='The permalink to the comment sample')
    mhs_score = models.FloatField(default=0, help_text='The mhs inference score of the sample')
    comment_body = models.TextField(help_text='The comment sample')
    username = models.CharField(max_length=32, help_text='The username of the commentor')

    def __str__(self):
        return f"Post By: {self.username} in: {self.subreddit.display_name}.\nScore: {self.mhs_score}.\nText: {self.comment_body}"


class Author_edge(models.Model):
    class Meta:
        db_table = 'toxit_author_edge'
        managed = False

    from_sub = models.ForeignKey(Subreddit_result, related_name='auth_from_sub', on_delete=models.CASCADE)
    to_sub = models.ForeignKey(Subreddit_result, related_name='auth_to_sub', on_delete=models.CASCADE)
    inference_task = models.ForeignKey(Inference_task, on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(help_text="The weight of the edge")

    def __str__(self):
        return f"Authors in common between {self.from_sub} and {self.to_sub} = {self.weight}"


class Mod_edge(models.Model):
    class Meta:
        db_table = 'toxit_mod_edge'
        managed = False

    from_sub = models.ForeignKey(Subreddit_result, related_name='mod_from_sub', on_delete=models.CASCADE)
    to_sub = models.ForeignKey(Subreddit_result, related_name='mod_to_sub', on_delete=models.CASCADE)
    inference_task = models.ForeignKey(Inference_task, on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(help_text="The weight of the edge")
 
    def __str__(self):
        return f"Mods in common between {self.from_sub} and {self.to_sub} = {self.weight}"