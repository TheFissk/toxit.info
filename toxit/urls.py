from django.urls import path

from . import views

app_name = 'toxit'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_network_data/<int:snapshot_id>/', views.get_network_data, name='get_network_data'),
    path('export_data/<int:snapshot_id>/<str:file_type>/', views.export_data, name='export_data'),
    path('test404/', views.test_404, name='test_404'),
]

handler404 = 'toxit.views.custom_404'