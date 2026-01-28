from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import F
from .models import Player, Upgrade, PlayerUpgrade, DailyReward, PlayerDailyReward, Task, PlayerTask
from .serializers import (
    PlayerSerializer, UpgradeSerializer, PlayerUpgradeSerializer,
    DailyRewardSerializer, PlayerDailyRewardSerializer, TaskSerializer,
    PlayerTaskSerializer, ClickSerializer, UpgradePurchaseSerializer
)


# Player Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def player_profile(request):
    """
    Get player profile information
    """
    try:
        player = request.user.player
    except Player.DoesNotExist:
        # Create player profile if it doesn't exist
        player = Player.objects.create(user=request.user)
    
    # Update last login
    player.last_login = timezone.now()
    player.save()
    
    serializer = PlayerSerializer(player)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_player_state(request):
    """
    Sync client state with server
    """
    try:
        player = request.user.player
    except Player.DoesNotExist:
        return Response({'error': 'Player profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Validate and update player state
    energy = request.data.get('energy', player.energy)
    balance = request.data.get('balance', player.balance)
    
    # Validate energy (can't exceed max_energy)
    energy = min(energy, player.max_energy)
    
    # Update player state
    player.energy = energy
    player.balance = balance
    player.last_energy_update = timezone.now()
    player.save()
    
    serializer = PlayerSerializer(player)
    return Response(serializer.data)


# Click Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_click(request):
    """
    Process a click action
    """
    serializer = ClickSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        player = request.user.player
    except Player.DoesNotExist:
        return Response({'error': 'Player profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    clicks = serializer.validated_data['clicks']
    client_energy = serializer.validated_data['energy']
    client_balance = serializer.validated_data['balance']
    timestamp = serializer.validated_data['timestamp']
    
    # Validate energy
    if player.energy < clicks:
        return Response({'error': 'Not enough energy'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Validate timestamp (should be recent)
    time_diff = abs((timezone.now() - timestamp).total_seconds())
    if time_diff > 30:  # More than 30 seconds old
        return Response({'error': 'Invalid timestamp'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Update player
    player.energy -= clicks
    player.balance += clicks * player.coins_per_click
    player.last_energy_update = timezone.now()
    player.save()
    
    # Return updated player state
    serializer = PlayerSerializer(player)
    return Response(serializer.data)


# Upgrade Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_upgrades(request):
    """
    List all available upgrades
    """
    upgrades = Upgrade.objects.filter(is_active=True)
    serializer = UpgradeSerializer(upgrades, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_upgrade(request):
    """
    Purchase an upgrade
    """
    serializer = UpgradePurchaseSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        player = request.user.player
    except Player.DoesNotExist:
        return Response({'error': 'Player profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    upgrade_id = serializer.validated_data['upgrade_id']
    expected_cost = serializer.validated_data['expected_cost']
    
    try:
        upgrade = Upgrade.objects.get(id=upgrade_id, is_active=True)
    except Upgrade.DoesNotExist:
        return Response({'error': 'Upgrade not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Get current upgrade level for player
    player_upgrade, created = PlayerUpgrade.objects.get_or_create(
        player=player, upgrade=upgrade,
        defaults={'level': 0}
    )
    
    # Calculate actual cost
    actual_cost = upgrade.get_cost(player_upgrade.level)
    if actual_cost is None:
        return Response({'error': 'Upgrade already at max level'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Validate expected cost matches actual cost
    if expected_cost != actual_cost:
        return Response({'error': 'Cost mismatch', 'actual_cost': actual_cost}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Check if player has enough coins
    if player.balance < actual_cost:
        return Response({'error': 'Not enough coins'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Process purchase
    player.balance -= actual_cost
    player_upgrade.level += 1
    player_upgrade.purchased_at = timezone.now()
    player_upgrade.save()
    player.save()
    
    # Apply upgrade effect
    if upgrade.upgrade_type == 'coins_per_click':
        player.coins_per_click += upgrade.base_effect_value + (upgrade.effect_per_level * (player_upgrade.level - 1))
    elif upgrade.upgrade_type == 'max_energy':
        player.max_energy += upgrade.base_effect_value + (upgrade.effect_per_level * (player_upgrade.level - 1))
        # Restore energy to new max if it was at max
        if player.energy == player.max_energy - upgrade.base_effect_value:
            player.energy = player.max_energy
    elif upgrade.upgrade_type == 'energy_regen':
        player.energy_regen_rate += upgrade.base_effect_value + (upgrade.effect_per_level * (player_upgrade.level - 1))
    
    player.save()
    
    # Return updated player and upgrade info
    player_serializer = PlayerSerializer(player)
    upgrade_serializer = PlayerUpgradeSerializer(player_upgrade)
    
    return Response({
        'player': player_serializer.data,
        'upgrade': upgrade_serializer.data
    })


# Daily Reward Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def daily_rewards_status(request):
    """
    Get daily reward status
    """
    try:
        player = request.user.player
    except Player.DoesNotExist:
        return Response({'error': 'Player profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Get all rewards
    rewards = DailyReward.objects.all()
    rewards_serializer = DailyRewardSerializer(rewards, many=True)
    
    # Get player's claimed rewards
    player_rewards = PlayerDailyReward.objects.filter(player=player)
    player_rewards_serializer = PlayerDailyRewardSerializer(player_rewards, many=True)
    
    return Response({
        'rewards': rewards_serializer.data,
        'player_rewards': player_rewards_serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def claim_daily_reward(request):
    """
    Claim daily reward
    """
    try:
        player = request.user.player
    except Player.DoesNotExist:
        return Response({'error': 'Player profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Determine which day reward to give (based on last claim)
    last_claim = PlayerDailyReward.objects.filter(player=player).order_by('-claimed_at').first()
    
    if last_claim:
        # Check if already claimed today
        if last_claim.claimed_at.date() == timezone.now().date():
            return Response({'error': 'Reward already claimed today'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate next day
        next_day = last_claim.reward.day + 1
    else:
        # First claim
        next_day = 1
    
    try:
        reward = DailyReward.objects.get(day=next_day)
    except DailyReward.DoesNotExist:
        # Reset to day 1 if sequence is broken
        reward = DailyReward.objects.get(day=1)
    
    # Award reward
    if reward.reward_type == 'coins':
        player.balance += reward.reward_amount
        player.save()
    
    # Record claim
    player_reward = PlayerDailyReward.objects.create(
        player=player,
        reward=reward,
        is_consecutive=last_claim is not None and last_claim.reward.day == next_day - 1
    )
    
    # Return updated player and reward info
    player_serializer = PlayerSerializer(player)
    reward_serializer = PlayerDailyRewardSerializer(player_reward)
    
    return Response({
        'player': player_serializer.data,
        'reward': reward_serializer.data
    })


# Task Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tasks(request):
    """
    List all tasks with player progress
    """
    try:
        player = request.user.player
    except Player.DoesNotExist:
        return Response({'error': 'Player profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Get all active tasks
    tasks = Task.objects.filter(is_active=True)
    
    # Get player's task progress
    player_tasks = PlayerTask.objects.filter(player=player, task__in=tasks)
    player_tasks_dict = {pt.task_id: pt for pt in player_tasks}
    
    # Prepare response data
    task_data = []
    for task in tasks:
        player_task = player_tasks_dict.get(task.id)
        if player_task:
            task_serializer = PlayerTaskSerializer(player_task)
        else:
            # Create a default player task
            player_task = PlayerTask(player=player, task=task)
            task_serializer = PlayerTaskSerializer(player_task)
        task_data.append(task_serializer.data)
    
    return Response(task_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def claim_task_reward(request):
    """
    Claim reward for completed task
    """
    try:
        player = request.user.player
    except Player.DoesNotExist:
        return Response({'error': 'Player profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    task_id = request.data.get('task_id')
    if not task_id:
        return Response({'error': 'task_id is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        task = Task.objects.get(id=task_id, is_active=True)
        player_task, created = PlayerTask.objects.get_or_create(
            player=player, task=task,
            defaults={'progress': 0, 'is_completed': False}
        )
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Check if task is completed
    if not player_task.is_completed:
        return Response({'error': 'Task not completed'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Check if reward already claimed
    if player_task.completed_at is not None:
        return Response({'error': 'Reward already claimed'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Award reward
    player.balance += task.reward_coins
    player.energy = min(player.energy + task.reward_energy, player.max_energy)
    player.save()
    
    # Mark reward as claimed
    player_task.completed_at = timezone.now()
    player_task.save()
    
    # Return updated player and task info
    player_serializer = PlayerSerializer(player)
    task_serializer = PlayerTaskSerializer(player_task)
    
    return Response({
        'player': player_serializer.data,
        'task': task_serializer.data
    })
