from django.urls import path
from django.contrib.auth import views as auth_views

from . import dash_views, views

app_name = 'toxit'
urlpatterns = [
    path('', views.index, name='index'),
    path('update_data/<int:snapshot_id>/',
         views.update_data, name='update_data'),
    path('dash/', dash_views.dash, name='dash'),
    path('login/', auth_views.LoginView.as_view(template_name='dash/login.html',
         next_page='/dash'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='../'), name='logout'),
    path('add_inference_task/', dash_views.add_Inference_Task, name='add_Inference_Task'),
    path('delete_inference_task/<task_id>', dash_views.delete_Inference_Task, name='delete_Inference_Task')
]
