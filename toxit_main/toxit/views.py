from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Node, Edge

def index(request):
    template = loader.get_template('toxit/index.html')

    nodes = Node.objects.all()
    edges = Edge.objects.all()

    context = {
        'nodes': nodes,
        'edges': edges,
    }

    return render(request, 'toxit/index.html', context)