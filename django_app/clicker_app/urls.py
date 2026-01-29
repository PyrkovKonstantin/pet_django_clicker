from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'clicker'

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('upgrades/', views.upgrades, name='upgrades'),
    path('daily-reward/', views.daily_reward, name='daily_reward'),
    path('click/', views.process_click, name='click'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='clicker/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]