from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from clicker_app import views as clicker_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    
    # Clicker app API endpoints
    path('api/player/', clicker_views.player_profile, name='player_profile'),
    path('api/player/sync/', clicker_views.sync_player_state, name='sync_player_state'),
    path('api/click/', clicker_views.process_click, name='process_click'),
    path('api/upgrades/', clicker_views.list_upgrades, name='list_upgrades'),
    path('api/upgrades/purchase/', clicker_views.purchase_upgrade, name='purchase_upgrade'),
    path('api/daily-rewards/', clicker_views.daily_rewards_status, name='daily_rewards_status'),
    path('api/daily-rewards/claim/', clicker_views.claim_daily_reward, name='claim_daily_reward'),
    path('api/tasks/', clicker_views.list_tasks, name='list_tasks'),
    path('api/tasks/claim/', clicker_views.claim_task_reward, name='claim_task_reward'),
]