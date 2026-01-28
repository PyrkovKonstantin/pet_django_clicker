from django.core.management.base import BaseCommand
from clicker_app.models import Player, Upgrade, PlayerUpgrade, DailyReward, Task, PlayerTask


class Command(BaseCommand):
    help = 'Show game statistics'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Clicker Game Statistics ===')
        )

        # Player statistics
        total_players = Player.objects.count()
        self.stdout.write(f'Total Players: {total_players}')

        if total_players > 0:
            top_player = Player.objects.order_by('-balance').first()
            self.stdout.write(f'Top Player: {top_player.username} (Balance: {top_player.balance})')

        # Upgrade statistics
        total_upgrades = Upgrade.objects.count()
        self.stdout.write(f'Total Upgrades: {total_upgrades}')

        total_player_upgrades = PlayerUpgrade.objects.count()
        self.stdout.write(f'Total Player Upgrades: {total_player_upgrades}')

        if total_player_upgrades > 0:
            most_upgraded = PlayerUpgrade.objects.order_by('-level').first()
            self.stdout.write(f'Most Upgraded: {most_upgraded.upgrade.name} (Level {most_upgraded.level})')

        # Daily reward statistics
        total_rewards = DailyReward.objects.count()
        self.stdout.write(f'Total Daily Rewards: {total_rewards}')

        # Task statistics
        total_tasks = Task.objects.count()
        self.stdout.write(f'Total Tasks: {total_tasks}')

        total_player_tasks = PlayerTask.objects.count()
        completed_tasks = PlayerTask.objects.filter(is_completed=True).count()
        self.stdout.write(f'Total Player Tasks: {total_player_tasks}')
        self.stdout.write(f'Completed Tasks: {completed_tasks}')

        if total_tasks > 0:
            completion_rate = (completed_tasks / max(total_player_tasks, 1)) * 100
            self.stdout.write(f'Task Completion Rate: {completion_rate:.2f}%')

        self.stdout.write(
            self.style.SUCCESS('=== End of Statistics ===')
        )