from django import forms
from django.forms import ModelForm, DateTimeInput
from ..models import Inference_task


# class inference_task_form(forms.Form):
#     start_sched = forms.DateTimeField(label="Start Time:")
#     time_scale = forms.ChoiceField(choices=Inference_task.TIME_SCALES)
#     min_words = forms.IntegerField(label='Min Words', min_value=0)
#     per_post_n = forms.IntegerField(label='Comments per Post:', min_value=1)
#     comments_n = forms.IntegerField(label='Comments per Subreddit:', min_value=1)
#     subreddit_set = forms.CharField(label='Subreddit set:', widget=forms.Textarea)

class MyDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    localize=False

class inference_task_form(ModelForm):
    class Meta:
        model = Inference_task
        fields = ['start_sched','time_scale', 'min_words', 'per_post_n', 'comments_n', 'subreddit_set']
        widgets = {'start_sched': DateTimeInput(attrs={'type': 'date'}),}