from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Inference_task

def update_data(request, snapshot_id):
    # Get the selected snapshot
    snapshot = get_object_or_404(Inference_task, id=snapshot_id)

    # Get the Subreddit_results for the selected snapshot
    subreddit_results = snapshot.get_subreddits_for_inference_task()

    # Prepare the data to be returned
    nodes_subr = [(result.subreddit.name, result.subreddit.name) for result in subreddit_results]
    edges_mods = [(result.subreddit.name, result.min_result) for result in subreddit_results if result.min_result is not None]
    edges_auth = [(result.subreddit.name, result.max_result) for result in subreddit_results if result.max_result is not None]
    data = {'nodes_': nodes_subr, 'edges_m': edges_mods, 'edges_a': edges_auth}

    # Return the data as a JSON response
    return JsonResponse(data)

def index(request):
    template = loader.get_template('toxit/index.html')

    # Get the selected snapshot
    snapshot_id = request.GET.get('snapshot_id')
    snapshot = get_object_or_404(Inference_task, id=snapshot_id) if snapshot_id else Inference_task.objects.first()

    context = {
        'snapshot': snapshot,
    }

    return render(request, 'toxit/index.html', context)