from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Inference_task


def dash(request):
    bounceNonLoggedInUsers(request.user)

    tasks = Inference_task.objects.all().order_by('-start_sched')

    context = {'iTasks': [
        {'start': t.start_sched, 'status':    Inference_task.STATUS_TYPES[t.status][1]} for t in tasks]}
    return render(request, 'dash\dash.html', context)


def add_Inference_Task(request):
    bounceNonLoggedInUsers(request.user)
    print('fire')
    print(request)
    return redirect('toxit:dash')


def bounceNonLoggedInUsers(user):
    if not user.is_authenticated:
        return redirect('toxit:login')
