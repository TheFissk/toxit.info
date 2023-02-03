# Generated by Django 4.1.5 on 2023-02-03 19:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inference_task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_sched', models.DateTimeField(help_text='Requested start time')),
                ('time_scale', models.CharField(choices=[('hour', 'This Hour'), ('day', 'Today'), ('week', 'This Week'), ('month', 'This Month'), ('year', 'This Year'), ('all', 'All Time')], help_text='The period overwhich the comments will be harvested', max_length=5)),
                ('min_words', models.IntegerField(default=20, help_text='The minimum number of words to be considered a valid comment', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(168)])),
                ('forest_width', models.IntegerField(default=10, help_text='The number of comments per level to be acquired', validators=[django.core.validators.MinValueValidator(0)])),
                ('per_post_n', models.IntegerField(default=1000, help_text='The maximum number of comments per post to be harvested', validators=[django.core.validators.MinValueValidator(1)])),
                ('comments_n', models.IntegerField(default=1000, help_text='The number of comments to be harvested', validators=[django.core.validators.MinValueValidator(1)])),
                ('subreddit_set', models.JSONField(help_text='A set of the subreddits to be harvested')),
                ('status', models.PositiveSmallIntegerField(choices=[('0', 'Scheduled'), ('1', 'In Progress'), ('2', 'Completed'), ('3', 'Error'), ('4', 'Cancelled')], help_text='The status of the task')),
            ],
        ),
        migrations.CreateModel(
            name='Subreddit',
            fields=[
                ('custom_id', models.CharField(help_text='Custom key from reddit', max_length=20, primary_key=True, serialize=False, unique=True)),
                ('display_name', models.CharField(help_text='Display name of the subreddit', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Subreddit_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_result', models.FloatField(blank=True, help_text='The minimum score from this subreddit', null=True)),
                ('max_result', models.FloatField(blank=True, help_text='The maxmimum score from this subreddit', null=True)),
                ('mean_result', models.FloatField(blank=True, help_text='The average score from this subreddit', null=True)),
                ('std_result', models.FloatField(blank=True, help_text='The standard deviation for this subreddit', null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='The time when the data was collected')),
                ('edges', models.JSONField(help_text='The edges for this subreddit')),
                ('inference_task', models.ForeignKey(help_text='The inference task in which this data was collected', on_delete=django.db.models.deletion.CASCADE, to='toxit.inference_task')),
                ('subreddit', models.ForeignKey(help_text='The subreddit that was analyzed', on_delete=django.db.models.deletion.CASCADE, to='toxit.subreddit')),
            ],
        ),
        migrations.CreateModel(
            name='Subreddit_mod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='The username of the moderator', max_length=32)),
                ('subreddit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toxit.subreddit')),
                ('subreddit_result', models.ForeignKey(help_text='The collection that the user was a moderator during', on_delete=django.db.models.deletion.CASCADE, to='toxit.subreddit_result')),
            ],
        ),
        migrations.CreateModel(
            name='Comment_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permalink', models.TextField(help_text='The permalink to the comment sample')),
                ('mhs_score', models.FloatField(default=0, help_text='The mhs inference score of the sample')),
                ('comment_body', models.TextField(help_text='The comment sample')),
                ('username', models.CharField(help_text='The username of the commentor', max_length=32)),
                ('subreddit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toxit.subreddit')),
                ('subreddit_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toxit.subreddit_result')),
            ],
        ),
    ]
