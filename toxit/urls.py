from django.urls import path
from django.contrib.auth import views as auth_views

from .dash_views import page_views, redirect_views

from . import views

app_name = 'toxit'
urlpatterns = [
    path('', views.index, name='index'),
    path('update_data/<int:snapshot_id>/',
         views.update_data, name='update_data'),
    path('dash/', page_views.dash, name='dash'),
    path('login/', auth_views.LoginView.as_view(template_name='dash/login.html',
         next_page='/dash'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='../'), name='logout'),
    path('delete_inference_task/<int:task_id>',
         redirect_views.delete_Inference_Task, name='delete_Inference_Task'),
    path('taskInspector/<int:task_id>',
         page_views.inspect_inference_task, name='taskInspector'),
    path('get_sub_data/<int:task_id>',
         page_views.get_subreddit_data, name='get_sub_data'),
]
