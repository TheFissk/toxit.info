import os
from django.http import JsonResponse, Http404, FileResponse
from tqdm import tqdm
from django.shortcuts import render, get_object_or_404

from .models import Inference_task
from .exportFactory import ExporterFactory


# custom 404 code based on https://codepen.io/tmrDevelops/embed/aNGKzN/?theme-id=modal#result-box
def custom_404(request, exception):
    return render(request, '404.html', status=404)


def test_404(request):
    raise Http404("This page does not exist")


def build_network_data(snapshot_id):
    # Get the selected snapshot
    snapshot = get_object_or_404(Inference_task, id=snapshot_id)

    # Get the Subreddit_results for the selected snapshot
    queried_subs = snapshot.get_subreddits_for_inference_task()
    queried_mods = snapshot.get_mod_edges_for_inference_task()
    queried_authors = snapshot.get_author_edges_for_inference_task()

    node_above_threshold = -0.05
    tooltip_precision = 6  # number of decimal places to round to

    # if you get any errors make sure tqdm is installed
    sub_nodes_context = [
        {
            'id': result.id,
            'label': f'r/{result.subreddit.display_name}'.center(22) + f'\n\n{result.getNodeInfo(node_above_threshold)}',
            # title = on hover visjs node tooltip
            'title': (
                f'r/{result.subreddit.display_name}\n'
                f'{"~".center(24, "~")}\n\n'
                f'Comments Above 0.05: {result.getNodeInfo(node_above_threshold)}\n\n'
                f'Min: {-1.0 * round(result.min_result, tooltip_precision)}\n'
                f'Max: {-1.0 * round(result.max_result, tooltip_precision)}\n'
                f'Mean: {-1.0 * round(result.mean_result, tooltip_precision)}\n'
                f'Std: {-1.0 * round(result.std_result, tooltip_precision)}\n'
            ),
            'subname': f'{result.subreddit.display_name}',
            'score': result.getNodeInfo(node_above_threshold),
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
    return data


def get_network_data(request, snapshot_id):
    network_data = build_network_data(snapshot_id)
    return JsonResponse(network_data)


def export_data(request, snapshot_id, file_type):
    # Get network data
    network_data = build_network_data(snapshot_id)

    # Create file using factory
    factory = ExporterFactory()
    file = factory.create_exporter(file_type).export(network_data)

    # Return file as a response
    response = FileResponse(file, content_type=file.content_type, as_attachment=True, filename=file.filename)
    return response


def index(request):
    # get a list of all inference tasks that have the STATUS_TYPE of ('2', 'Completed') defined in the models
    iTasks = Inference_task.objects.filter(
        status=Inference_task.STATUS_TYPES[2][0]
    ).order_by('-start_sched')

    # get a list of all image filenames in the BG-Pic directory
    path = 'toxit/static/BG-Pic'
    images = os.listdir(path)

    context = {
        'iTasks': iTasks,
        'images': images,
    }

    return render(request, 'toxit/index.html', context)
