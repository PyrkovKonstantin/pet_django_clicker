from django.urls import path
from . import views

app_name = 'clicker'

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('upgrades/', views.upgrades, name='upgrades'),
    path('daily-reward/', views.daily_reward, name='daily_reward'),
    path('click/', views.process_click, name='click'),
]