from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest
from ..models import Inference_task


def add_Inference_Task(request) -> HttpResponseRedirect:
    if not request.user.is_authenticated:
        return redirect('toxit:login')
    print('fire')
    post = request.POST
    newTask = Inference_task(
        start_sched=post['start_sched'],
        min_words=post['min_words'],
        per_post_n=post['comments_per_post'],
        comments_n=post['comments_n'],
        subreddit_set=post['subreddit_set'],
        status=0,
    )
    newTask.save()
    return redirect('toxit:dash')


def delete_Inference_Task(request, task_id) -> HttpResponseRedirect:
    if not request.user.is_authenticated:
        return redirect('toxit:login')
    if request.method == 'POST':
      print("fire")  
      task = get_object_or_404(Inference_task, id=task_id)
      task.delete()
    return redirect('toxit:dash')
