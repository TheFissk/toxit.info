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
    t0_options = [(result.subreddit.name, result.subreddit.name) for result in subreddit_results]
    t1_options = [(result.subreddit.name, result.min_result) for result in subreddit_results if result.min_result is not None]
    t2_options = [(result.subreddit.name, result.max_result) for result in subreddit_results if result.max_result is not None]
    data = {'t0Options': t0_options, 't1Options': t1_options, 't2Options': t2_options}

    # Return the data as a JSON response
    return JsonResponse(data)

def index(request):
    template = loader.get_template('toxit/index.html')

    # Fetch all Inference_task objects and their related Subreddit_result objects
    I_t = Inference_task.objects.prefetch_related('subreddit_result_set').all()

    context = {
        'Snapshots': I_t,
    }

    return render(request, 'toxit/index.html', context)