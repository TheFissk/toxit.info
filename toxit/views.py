import os
from django.http import HttpResponse, JsonResponse
from tqdm import tqdm
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


    precision = 6  # number of decimal places to round to

    # if you get any errors make sure tqdm is installed 
    sub_nodes_context = [
        {
            'id': result.id, 
            'label': f'r/{result.subreddit.display_name}\n[{round(result.mean_result, 3)}]',
            # title = on hover visjs node tooltip
            'title': (
                f'r/{result.subreddit.display_name}\n'
                f'{"~".center(len(result.subreddit.display_name) + 6, "~")}\n'
                f'Min: {round(result.min_result, precision)}\n'
                f'Max: {round(result.max_result, precision)}\n'
                f'Mean: {round(result.mean_result, precision)}\n'
                f'Std: {round(result.std_result, precision)}'
            ),
            'subname': f'r/{result.subreddit.display_name}',
            'score': result.mean_result,
        } for result in tqdm(queried_subs, desc='Sub Nodes')
    ]
    mod_edges_context = [
        {
            'from': result.from_sub_id,
            'to': result.to_sub_id,
            'label': str(result.weight),
        } for result in tqdm(queried_mods, desc='Mod Edges')
    ]
    author_edges_context = [
        {
            'from': result.from_sub_id,
            'to': result.to_sub_id,
            'label': str(result.weight),
        } for result in tqdm(queried_authors, desc='Author Edges')
    ]

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
    iTasks = Inference_task.objects.filter(
        status=Inference_task.STATUS_TYPES[2][0])

    # get a list of all image filenames in the BG-Pic directory
    path = 'toxit/static/BG-Pic'
    images = os.listdir(path)

    context = {
        'iTasks': iTasks,
        'images': images,
    }

    return render(request, 'toxit/index.html', context)
