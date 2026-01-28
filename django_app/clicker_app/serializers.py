from rest_framework import serializers
from .models import Player, Upgrade, PlayerUpgrade, DailyReward, PlayerDailyReward, Task, PlayerTask, Referral


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'id', 'username', 'balance', 'level', 'energy', 'max_energy',
            'energy_regen_rate', 'coins_per_click', 'last_login', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'last_login']


class UpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upgrade
        fields = [
            'id', 'name', 'description', 'icon', 'base_cost', 'cost_multiplier',
            'upgrade_type', 'base_effect_value', 'effect_per_level', 'max_level',
            'is_active', 'order'
        ]


class PlayerUpgradeSerializer(serializers.ModelSerializer):
    upgrade = UpgradeSerializer(read_only=True)
    
    class Meta:
        model = PlayerUpgrade
        fields = ['id', 'upgrade', 'level', 'purchased_at']


class DailyRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReward
        fields = ['id', 'day', 'reward_type', 'reward_amount', 'is_special']


class PlayerDailyRewardSerializer(serializers.ModelSerializer):
    reward = DailyRewardSerializer(read_only=True)
    
    class Meta:
        model = PlayerDailyReward
        fields = ['id', 'reward', 'claimed_at', 'is_consecutive']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'task_type', 'target_value',
            'reward_coins', 'reward_energy', 'is_active', 'order'
        ]


class PlayerTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    
    class Meta:
        model = PlayerTask
        fields = ['id', 'task', 'progress', 'is_completed', 'completed_at']


class ReferralSerializer(serializers.ModelSerializer):
    referrer = PlayerSerializer(read_only=True)
    referred = PlayerSerializer(read_only=True)
    
    class Meta:
        model = Referral
        fields = ['id', 'referrer', 'referred', 'created_at', 'reward_claimed']


class ClickSerializer(serializers.Serializer):
    clicks = serializers.IntegerField(min_value=1, max_value=100)
    timestamp = serializers.DateTimeField()
    energy = serializers.IntegerField()
    balance = serializers.IntegerField()


class UpgradePurchaseSerializer(serializers.Serializer):
    upgrade_id = serializers.IntegerField()
    expected_cost = serializers.IntegerField()