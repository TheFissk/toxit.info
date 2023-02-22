from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Inference_task


def update_data(request, snapshot_id):
    # Get the selected snapshot
    snapshot = get_object_or_404(Inference_task, id=snapshot_id)

    # Get the Subreddit_results for the selected snapshot
    queried_subs = snapshot.get_subreddits_for_inference_task()
    queried_mods = snapshot.get_mod_edges_for_inference_task()
    queried_authors = snapshot.get_author_edges_for_inference_task()

    # Prepare the data to be returned
    sub_nodes_context = [
        {
            'id': result.subreddit.custom_id, 
            'label': result.subreddit.display_name
        } for result in queried_subs
    ]
    mod_edges_context = [
        {
            'from': result.from_sub.subreddit.custom_id,
            'to': result.to_sub.subreddit.custom_id,
            'label': str(result.weight),
        } for result in queried_mods
    ]
    author_edges_context = [
        {
            'from': result.from_sub.subreddit.custom_id, 
            'to': result.to_sub.subreddit.custom_id
        } for result in queried_authors
    ]
    
    # debug print
    print(mod_edges_context)  # add this line to log the mod_edges_context list

    data = {
        'sub_nodes_context': sub_nodes_context,
        'mod_edges_context': mod_edges_context,
        'author_edges_context': author_edges_context,
    }

    # Return the data as a JSON response
    return JsonResponse(data)


def index(request):
    template = loader.get_template('toxit/index.html')

    # get a list of all inference tasks that have the STATUS_TYPE of ('2', 'Completed') defined in the models
    iTasks = Inference_task.objects.filter(status=Inference_task.STATUS_TYPES[2][0])

    context = {
        'iTasks': iTasks,
    }

    return render(request, 'toxit/index.html', context)