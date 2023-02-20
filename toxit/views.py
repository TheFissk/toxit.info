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
    sub_nodes_context = [(result.subreddit.name, result.subreddit.name) for result in subreddit_results]
    mod_edges_context = [(result.subreddit.name, result.min_result) for result in subreddit_results if result.min_result is not None]
    autor_edges_context = [(result.subreddit.name, result.max_result) for result in subreddit_results if result.max_result is not None]
    data = {'sub_nodes_context': sub_nodes_context, 'mod_edges_context': mod_edges_context, 'autor_edges_context': autor_edges_context}

    # Return the data as a JSON response
    return JsonResponse(data)

def index(request):
    template = loader.get_template('toxit/index.html')

    # all 
    iTasks = Inference_task.objects.all()

    # Get the selected snapshot
    selected = Inference_task.objects.first()

    context = {
        'iTasks': iTasks,
    }

    return render(request, 'toxit/index.html', context)