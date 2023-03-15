from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from ..models import Inference_task
from .inference_task_form import inference_task_form


def dash(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('toxit:login')

    # handle a form submission
    if request.method == 'POST':
        form = inference_task_form(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
        return redirect('toxit:dash')
    else:
        print("else")
        form = inference_task_form()

    tasks = Inference_task.objects.all().order_by('-start_sched')

    context = {
        'iTasks': [
            {'id': t.id, 'start': t.start_sched,
             'status': Inference_task.STATUS_TYPES[t.status][1]}
            for t in tasks],
        'form': form}
    return render(request, 'dash\dash.html', context)


def inspect_inference_task(request, task_id) -> HttpResponse:
    task = Inference_task.objects.get(id=task_id)
    context = {
        "task": task
    }
    return render(request, 'dash\inspector.html', context)
