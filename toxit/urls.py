from django.urls import path
from django.contrib.auth import views as auth_views

from .dash_views import page_views, redirect_views

from . import views

app_name = 'toxit'

urlpatterns = [
    # landing page
    path('', views.landing, name='landing'),
    
    # VisJS Graph (with factory + observer)
    path('index', views.index, name='index'),
    # url for updated visjs data with ajax call
    path('get_network_data/<int:snapshot_id>/', views.get_network_data, name='get_network_data'),
    # url for factory export design pattern using ajax
    path('export_data/<int:snapshot_id>/<str:file_type>/', views.export_data, name='export_data'),
    # support function for gathering data used by other methods
    path('update_data/<int:snapshot_id>/', views.get_network_data, name='update_data'),
    # dash admin panel 
    path('dash/', page_views.dash, name='dash'), 
    path('login/', auth_views.LoginView.as_view(template_name='dash/login.html', next_page='/dash'), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='../'), name='logout'),
    path('delete_inference_task/<int:task_id>', redirect_views.delete_Inference_Task, name='delete_Inference_Task'),
    path('taskInspector/<int:task_id>', page_views.inspect_inference_task, name='taskInspector'),
    path('get_sub_data/<int:task_id>', page_views.get_subreddit_data, name='get_sub_data'),
    # Custom 404 
    path('test404/', views.test_404, name='test_404'),
]

handler404 = 'toxit.views.custom_404'