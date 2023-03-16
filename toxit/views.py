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


    node_above_threshold = 0.02

    sub_nodes = [
        {'id': result.id,
         'name': result.subreddit.display_name,
         'flaggedComments': result.getNodeInfo(node_above_threshold),
         'min': result.min_result,
         'max': result.max_result,
         'mean': result.mean_result,
         'std': result.std_result, }
        for result in tqdm(queried_subs, desc='Sub Nodes')
    ]

    # if you get any errors make sure tqdm is installed

    mod_edges = [
        {
            'from': result.from_sub_id,
            'to': result.to_sub_id,
            'label': str(result.weight),
        } for result in tqdm(queried_mods, desc='Mod Edges')
    ]
    author_edges = [
        {
            'from': result.from_sub_id,
            'to': result.to_sub_id,
            'label': str(result.weight),
        } for result in tqdm(queried_authors, desc='Author Edges')
    ]

    data = {
        'sub_nodes_context': sub_nodes,
        'mod_edges_context': mod_edges,
        'author_edges_context': author_edges,
    }
    return data


def get_network_data(request, snapshot_id=None):
    if snapshot_id is None:
        # If no snapshot_id is specified, get the latest completed snapshot
        snapshot = Inference_task.objects.filter(
            status=Inference_task.STATUS_TYPES[2][0]
        ).order_by('-start_sched').first()
        if snapshot is None:
            return Http404('No completed snapshots found')
        snapshot_id = snapshot.id
    network_data = build_network_data(snapshot_id)

    tooltip_precision = 6
    sub_nodes_context = [
        {
            'id': result["id"],
            'label': f'r/{result["name"]}'.center(22) + f'\n\n{result["flaggedComments"]}',
            # title = on hover visjs node tooltip
            'title': (
                f'r/{result["name"]}\n'
                f'{"~".center(24, "~")}\n\n'
                f'Comments Above 0.05: {result["flaggedComments"]}\n\n'
                f'Min: {-1.0 * round(result["min"], tooltip_precision)}\n'
                f'Max: {-1.0 * round(result["max"], tooltip_precision)}\n'
                f'Mean: {-1.0 * round(result["mean"], tooltip_precision)}\n'
                f'Std: {-1.0 * round(result["std"], tooltip_precision)}\n'
            ),
            'subname': result['name'],
            'score': result['flaggedComments'],
        } for result in network_data['sub_nodes_context']
    ]

    data = {
        'sub_nodes_context': sub_nodes_context,
        'mod_edges_context': network_data['mod_edges_context'],
        'author_edges_context': network_data['author_edges_context'],
    }

    return JsonResponse(data)


def export_data(request, snapshot_id=None, file_type=None):
    if snapshot_id is None:
        # If no snapshot_id is specified, get the latest completed snapshot
        snapshot = Inference_task.objects.filter(
            status=Inference_task.STATUS_TYPES[2][0]
        ).order_by('-start_sched').first()
        if snapshot is None:
            return Http404('No completed snapshots found')
        snapshot_id = snapshot.id
    if file_type is None:
        return Http404('No file type specified')
    # Create network data using the snapshot_id
    network_data = build_network_data(snapshot_id)

    # Create file using factory
    exportFactory = ExporterFactory()
    exportFile = exportFactory.create_exporter(file_type, network_data)
    file = exportFile.export()

    # Return file as a response
    return file


def index(request, snapshot_id=None):
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
