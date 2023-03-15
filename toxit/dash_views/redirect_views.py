from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest
from ..models import Inference_task


def delete_Inference_Task(request, task_id) -> HttpResponseRedirect:
    if not request.user.is_authenticated:
        return redirect('toxit:login')

    print("fire")
    task = get_object_or_404(Inference_task, id=task_id)
    task.delete()
    return redirect('toxit:dash')
