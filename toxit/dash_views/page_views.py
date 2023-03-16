from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

from tqdm import tqdm

from ..models import Inference_task, Subreddit_result
from .inference_task_form import inference_task_form


def dash(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('toxit:login')

    # handle a form submission
    if request.method != 'POST':
        form = inference_task_form()
    else:
        form = inference_task_form(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('toxit:dash')


    tasks = Inference_task.objects.all().order_by('-start_sched')

    context = {
        'iTasks': [
            {'id': t.id, 'start': t.start_sched,
             'status': Inference_task.STATUS_TYPES[t.status][1]}
            for t in tasks],
        'form': form}
    return render(request, 'dash\dash.html', context)


def get_subreddit_data(request, task_id) -> JsonResponse:
    task = get_object_or_404(Inference_task, id=task_id)
    subs = Inference_task.get_subreddits_for_inference_task(task)
    out = {'subs': [{
        'name': s.subreddit.display_name,
        'min': s.min_result,
        'max': s.max_result,
        'mean': s.mean_result,
        'std': s.std_result,
    }for s in tqdm(subs)]}
    return JsonResponse(out)


def inspect_inference_task(request, task_id) -> HttpResponse:
    task = Inference_task.objects.get(id=task_id)
    context = {
        "task": task
    }
    return render(request, 'dash\inspector.html', context)
