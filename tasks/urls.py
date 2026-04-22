from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.email_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('home/', views.home, name='home'),
    path('tasks/', views.task_page, name='tasks'),
     path('add-task/', views.add_task_ajax, name='add_task_ajax'),

    # ✅ ADD THIS
    path('signup/', views.signup, name='signup'),

    # ✅ ADD THIS (for forgot password link)
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    path('delete/<int:id>/', views.delete_task, name='delete'),
    path('toggle/<int:id>/', views.toggle_task, name='toggle'),
]