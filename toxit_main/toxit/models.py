from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
        