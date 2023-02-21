from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Inference_task

def update_data(request, snapshot_id):
    # Get the selected snapshot
    snapshot = get_object_or_404(Inference_task, id=snapshot_id)

    # Get the Subreddit_results for the selected snapshot
    fetched_subs = snapshot.get_subreddits_for_inference_task()
    fetched_mods = snapshot.get_mod_edges_for_inference_task()
    fetched_authors = snapshot.get_author_edges_for_inference_task()

    # Prepare the data to be returned
    sub_nodes_context = [(result.subreddit_result) for result in fetched_subs]
    mod_edges_context = [(result.mod_edge.from_sub, result.mod_edge.to_sub) for result in fetched_mods]
    author_edges_context = [(result.author_edge.from_sub, result.author_edge.to_sub) for result in fetched_authors]
    data = {'sub_nodes_context': sub_nodes_context, 'mod_edges_context': mod_edges_context, 'autor_edges_context': author_edges_context}

    # Return the data as a JSON response
    return JsonResponse(data)

def index(request):
    template = loader.get_template('toxit/index.html')

    # grab all of the inference tasks
    iTasks = Inference_task.objects.all()

    # Get the selected inference task or snapshot; default first for now
    selected = Inference_task.objects.first()

    context = {
        'iTasks': iTasks,
    }

    return render(request, 'toxit/index.html', context)