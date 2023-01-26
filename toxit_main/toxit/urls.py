from django.urls import path

from . import views

app_name = 'toxit'
urlpatterns = [
    path('', views.index, name='index'),
]