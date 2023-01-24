from django.http import HttpResponse
from django.template import loader

# from .models import Question

def index(request):
    template = loader.get_template('toxit/index.html')
    return HttpResponse(template.render())