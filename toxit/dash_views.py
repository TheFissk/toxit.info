from django.shortcuts import render, redirect
from django.http import HttpResponse


def dash(request):
    if not request.user.is_authenticated:
        return redirect('toxit:login')
    return render(request, 'dash\dash.html')