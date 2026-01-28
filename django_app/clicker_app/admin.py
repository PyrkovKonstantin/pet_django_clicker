from django.contrib import admin
from .models import Player, Upgrade, PlayerUpgrade, DailyReward, PlayerDailyReward, Task, PlayerTask, Referral


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['username', 'user', 'balance', 'level', 'energy', 'last_login', 'created_at']
    list_filter = ['level', 'is_verified', 'created_at']
    search_fields = ['username', 'user__username']
    readonly_fields = ['created_at', 'last_login', 'last_energy_update']


@admin.register(Upgrade)
class UpgradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'upgrade_type', 'base_cost', 'max_level', 'is_active', 'order']
    list_filter = ['upgrade_type', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['order']


@admin.register(PlayerUpgrade)
class PlayerUpgradeAdmin(admin.ModelAdmin):
    list_display = ['player', 'upgrade', 'level', 'purchased_at']
    list_filter = ['upgrade', 'purchased_at']
    search_fields = ['player__username', 'upgrade__name']


@admin.register(DailyReward)
class DailyRewardAdmin(admin.ModelAdmin):
    list_display = ['day', 'reward_type', 'reward_amount', 'is_special']
    list_filter = ['reward_type', 'is_special']
    ordering = ['day']


@admin.register(PlayerDailyReward)
class PlayerDailyRewardAdmin(admin.ModelAdmin):
    list_display = ['player', 'reward', 'claimed_at', 'is_consecutive']
    list_filter = ['reward', 'is_consecutive', 'claimed_at']
    search_fields = ['player__username']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'task_type', 'target_value', 'reward_coins', 'is_active', 'order']
    list_filter = ['task_type', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['order']


@admin.register(PlayerTask)
class PlayerTaskAdmin(admin.ModelAdmin):
    list_display = ['player', 'task', 'progress', 'is_completed', 'completed_at']
    list_filter = ['task', 'is_completed']
    search_fields = ['player__username', 'task__name']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred', 'created_at', 'reward_claimed']
    list_filter = ['reward_claimed', 'created_at']
    search_fields = ['referrer__username', 'referred__username']
