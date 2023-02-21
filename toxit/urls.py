from django.urls import path

from . import views

app_name = 'toxit'
urlpatterns = [
    path('', views.index, name='index'),
    path('update_data/<int:snapshot_id>/', views.update_data, name='update_data'),
]