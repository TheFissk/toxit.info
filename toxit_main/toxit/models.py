from django.db import models
from django.core.exceptions import ValidationError

class Node(models.Model):
    subreddit_name = models.CharField(max_length=24) # regex = r"^([a-z0-9][_a-z0-9]{2,20})$"\n
    toxicity_score = models.FloatField(default=0)

    def __str__(self):
        return self.subreddit_name


class Edge(models.Model):
    start_node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name="start", help_text="Origin of edge")
    end_node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name="end", help_text="Destination of edge")
    shared_mod_count = models.PositiveIntegerField(default=0, help_text="Arc weight representing the number of shared moderators between subreddits.")
    shared_mod_sim = models.FloatField(default=0, help_text="Arc weight representing some magic stats number with a fancy name.")

    class Meta:
        unique_together = ('start_node', 'end_node')
    
    def validate_unique(self, exclude=None):
        if self.start_node == self.end_node:
            raise ValidationError("Node cannot refer to self.")
        super(Edge, self).validate_unique(exclude=exclude)

    def __str__(self):
        return str("from: " + self.start_node.subreddit_name + ", to: " + self.end_node.subreddit_name)

# START OF BACK END TEAM MODELS

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Subreddit(models.Model):
    custom_id = models.CharField(primary_key=True, max_length=20, unique=True)
    display_name = models.CharField(max_length=200)

class Subreddit_mod(models.Model):
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)

class Inference_task(models.Model):
    TIME_SCALES = [
        ('hour', 'This Hour'),
        ('day', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('year', 'This Year'),
        ('all', 'All Time')
    ]
    time_scale = models.CharField(max_length=5, choices=TIME_SCALES)
    start_sched = models.DateTimeField()
    min_words = models.IntegerField(default=3, validators= [ MaxValueValidator(168), MinValueValidator(3)])
    forest_width = models.IntegerField(default=1, validators= [ MaxValueValidator(100), MinValueValidator(0)])
    per_post_n = models.IntegerField(default=100, validators= [ MaxValueValidator(1000), MinValueValidator(100)])
    comments_n = models.IntegerField(default=100, validators= [ MaxValueValidator(1000), MinValueValidator(100)])
    subredit_set = models.JSONField()


class Subreddit_result(models.Model):
    inference_task = models.ForeignKey(Inference_task, on_delete=models.CASCADE)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    min = models.FloatField()
    max = models.FloatField()
    mean = models.FloatField()
    std = models.FloatField()

class Comment_author(models.Model):
    subreddit_result = models.ForeignKey(Subreddit_result, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)


class Comment_result(models.Model):
    subreddit_result = models.ForeignKey(Subreddit_result, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(Comment_author, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    score = models.FloatField()
