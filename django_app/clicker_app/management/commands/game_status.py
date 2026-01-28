from django.core.management.base import BaseCommand
from django.utils import timezone
from clicker_app.models import Player, Upgrade, Task, DailyReward


class Command(BaseCommand):
    help = 'Show current game status'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Clicker Game Status ===')
        )

        # Current time
        self.stdout.write(f'Current Time: {timezone.now()}')

        # Player statistics
        total_players = Player.objects.count()
        self.stdout.write(f'\nPlayers: {total_players}')

        if total_players > 0:
            # Balance statistics
            total_balance = sum(Player.objects.values_list('balance', flat=True))
            avg_balance = total_balance / total_players
            top_player = Player.objects.order_by('-balance').first()
            
            self.stdout.write(f'  Total Balance: {total_balance}')
            self.stdout.write(f'  Average Balance: {avg_balance:.2f}')
            self.stdout.write(f'  Top Player: {top_player.username} ({top_player.balance})')

            # Level statistics
            total_level = sum(Player.objects.values_list('level', flat=True))
            avg_level = total_level / total_players
            top_level_player = Player.objects.order_by('-level').first()
            
            self.stdout.write(f'  Average Level: {avg_level:.2f}')
            self.stdout.write(f'  Highest Level: {top_level_player.username} (Level {top_level_player.level})')

        # Upgrade statistics
        total_upgrades = Upgrade.objects.count()
        active_upgrades = Upgrade.objects.filter(is_active=True).count()
        self.stdout.write(f'\nUpgrades: {total_upgrades} (Active: {active_upgrades})')

        # Task statistics
        total_tasks = Task.objects.count()
        active_tasks = Task.objects.filter(is_active=True).count()
        self.stdout.write(f'Tasks: {total_tasks} (Active: {active_tasks})')

        # Daily reward statistics
        total_rewards = DailyReward.objects.count()
        self.stdout.write(f'Daily Rewards: {total_rewards}')

        # Recent activity
        self.stdout.write(f'\nRecent Activity:')
        recent_players = Player.objects.order_by('-last_login')[:5]
        if recent_players.exists():
            for player in recent_players:
                self.stdout.write(
                    f'  {player.username} logged in {player.last_login}'
                )
        else:
            self.stdout.write('  No recent activity')

        self.stdout.write(
            self.style.SUCCESS('=== End of Game Status ===')
        )