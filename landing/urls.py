from django.urls import path

from landing import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('task/<str:task_id>/', views.check_result, name='task'),

]