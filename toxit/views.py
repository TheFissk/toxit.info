from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render

from .models import Inference_task

def update_data(request, snap_id):
    snapshot = Inference_task.objects.get(id=snap_id)
    t0 = snapshot.get_subreddit_node_list()
    t1 = snapshot.get_subreddit_mod_edges()
    t2 = snapshot.get_subreddit_author_edges()

    t0Options = ""
    for t in t0:
        t0Options += f'<option value="{t.id}">test1 #{t.id}</option>'

    t1Options = ""
    for t in t1:
        t1Options += f'<option value="{t.id}">test2 #{t.id}</option>'

    t2Options = ""
    for t in t2:
        t2Options += f'<option value="{t.id}">test3 #{t.id}</option>'

    data = {'t0Options': t0Options, 't1Options': t1Options, 't2Options': t2Options}
    return JsonResponse(data)

def index(request):
    template = loader.get_template('toxit/index.html')

    I_t = Inference_task.objects.all()

    # Loop over Inference_task instances and call get_subreddit_node_list() on each
    for it in I_t:
        it.subreddit_node_list = it.get_subreddit_node_list()

    context = {
        'Snapshots': I_t,
    }

    return render(request, 'toxit/index.html', context)