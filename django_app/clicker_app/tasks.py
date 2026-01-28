from celery import shared_task
from django.utils import timezone
from django.db.models import F
from .models import Player
from datetime import timedelta


@shared_task
def regenerate_energy():
    """
    Regenerate energy for active players
    This task should be run periodically (e.g., every 30 seconds)
    """
    # Get players who were active recently (last 10 minutes)
    active_players = Player.objects.filter(
        last_energy_update__gte=timezone.now() - timedelta(minutes=10)
    )
    
    updated_count = 0
    
    for player in active_players:
        # Calculate seconds since last energy update
        seconds_since_update = (timezone.now() - player.last_energy_update).total_seconds()
        
        # Calculate energy to regenerate
        energy_to_regenerate = int(seconds_since_update * player.energy_regen_rate)
        
        # Only update if there's energy to regenerate
        if energy_to_regenerate > 0:
            # Update energy (but don't exceed max_energy)
            new_energy = min(player.max_energy, player.energy + energy_to_regenerate)
            
            # Only update if energy actually changed
            if new_energy != player.energy:
                player.energy = new_energy
                player.last_energy_update = timezone.now()
                player.save()
                updated_count += 1
    
    return f"Updated energy for {updated_count} players"


@shared_task
def reset_daily_rewards():
    """
    Reset daily rewards at midnight
    This task should be run daily at midnight
    """
    # This would handle any daily reset logic if needed
    # For now, we're handling daily rewards through the claim system
    pass


@shared_task
def update_leaderboard():
    """
    Update leaderboard cache
    This task should be run periodically (e.g., every 10 minutes)
    """
    # Get top 100 players by balance
    top_players = Player.objects.order_by('-balance')[:100]
    
    # In a real implementation, you would cache this data
    # For example, using Redis:
    # import redis
    # r = redis.Redis()
    # leaderboard_data = [
    #     {
    #         'id': player.id,
    #         'username': player.username,
    #         'balance': player.balance,
    #         'level': player.level
    #     } for player in top_players
    # ]
    # r.set('leaderboard', json.dumps(leaderboard_data), ex=600)  # Cache for 10 minutes
    
    return f"Updated leaderboard with {top_players.count()} players"


@shared_task
def update_task_progress():
    """
    Update player task progress
    This task should be run periodically (e.g., every hour)
    """
    # This would update task progress for all players
    # For example, counting total clicks, upgrades purchased, etc.
    
    # Example: Update click-based tasks
    # This is a simplified example - in practice you'd want to track clicks
    # in a separate model to avoid recalculating from scratch
    
    updated_tasks = 0
    
    # Get all click-based tasks
    # click_tasks = Task.objects.filter(task_type='clicks')
    
    # for task in click_tasks:
    #     # Update progress for all players
    #     for player in Player.objects.all():
    #         # Get player's total clicks (this would need to be tracked)
    #         total_clicks = player.total_clicks or 0
    #         
    #         # Update task progress
    #         player_task, created = PlayerTask.objects.get_or_create(
    #             player=player, task=task,
    #             defaults={'progress': 0, 'is_completed': False}
    #         )
    #         
    #         if not player_task.is_completed and total_clicks >= task.target_value:
    #             player_task.progress = total_clicks
    #             player_task.is_completed = True
    #             player_task.save()
    #             updated_tasks += 1
    #         elif player_task.progress != total_clicks:
    #             player_task.progress = total_clicks
    #             player_task.save()
    #             updated_tasks += 1
    
    return f"Updated progress for {updated_tasks} tasks"