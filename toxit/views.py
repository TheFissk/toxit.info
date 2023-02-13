from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Inference_task, Subreddit_result

def index(request):
    IT = Inference_task.objects.get(pk=21)
    Subreddits = IT.get_subreddits_for_inference_task()
    EdgeTable = IT.get_unique_edge_pairs()

    edge_data = []
    for edge in EdgeTable:
        edge_data.append({
            'from_Sub': edge[0][0],
            'to_Sub': edge[0][1],
            'label': edge[0][2]
        })

    context = {
        'subs': Subreddits,
        'edge_data': edge_data,
    }

    return render(request, 'toxit/index.html', context)