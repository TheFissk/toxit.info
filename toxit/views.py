from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Inference_task

def index(request):
    template = loader.get_template('toxit/index.html')

    IT = Inference_task.objects.get(pk=21)
    Subreddits = IT.get_subreddits_for_inference_task
    EdgeTable = IT.get_unique_edge_pairs

    context = {
        'subs': Subreddits,
        'test123': EdgeTable,
    }

    return render(request, 'toxit/index.html', context)