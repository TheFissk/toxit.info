from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Subreddit_result, Inference_task

def index(request):
    template = loader.get_template('toxit/index.html')

    IT = Inference_task.objects.get(pk=19)
    Subreddits = Subreddit_result.objects.filter(inference_task=IT)

    context = {
        'subs': Subreddits,
    }

    return render(request, 'toxit/index.html', context)