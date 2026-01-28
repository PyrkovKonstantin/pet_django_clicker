from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clicker_app.models import Player, PlayerUpgrade, PlayerDailyReward, PlayerTask


class Command(BaseCommand):
    help = 'Show detailed information about a player'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the player')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User {username} does not exist!')
            )
            return

        try:
            player = Player.objects.get(user=user)
        except Player.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Player for user {username} does not exist!')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'=== Player Information: {player.username} ===')
        )

        # Basic player info
        self.stdout.write(f'User ID: {user.id}')
        self.stdout.write(f'Player ID: {player.id}')
        self.stdout.write(f'Balance: {player.balance}')
        self.stdout.write(f'Level: {player.level}')
        self.stdout.write(f'Energy: {player.energy}/{player.max_energy}')
        self.stdout.write(f'Coins per Click: {player.coins_per_click}')
        self.stdout.write(f'Energy Regen Rate: {player.energy_regen_rate}')
        self.stdout.write(f'Created: {player.created_at}')
        self.stdout.write(f'Last Login: {player.last_login}')

        # Player upgrades
        self.stdout.write(f'\nUpgrades:')
        player_upgrades = PlayerUpgrade.objects.filter(player=player)
        if player_upgrades.exists():
            for pu in player_upgrades:
                self.stdout.write(
                    f'  {pu.upgrade.name}: Level {pu.level}'
                )
        else:
            self.stdout.write('  No upgrades purchased')

        # Daily rewards
        self.stdout.write(f'\nDaily Rewards:')
        player_rewards = PlayerDailyReward.objects.filter(player=player).order_by('-claimed_at')
        if player_rewards.exists():
            last_reward = player_rewards.first()
            self.stdout.write(
                f'  Last claimed: Day {last_reward.reward.day} on {last_reward.claimed_at}'
            )
        else:
            self.stdout.write('  No rewards claimed')

        # Tasks
        self.stdout.write(f'\nTasks:')
        player_tasks = PlayerTask.objects.filter(player=player)
        completed_tasks = player_tasks.filter(is_completed=True)
        self.stdout.write(f'  Total: {player_tasks.count()}')
        self.stdout.write(f'  Completed: {completed_tasks.count()}')
        
        if completed_tasks.exists():
            self.stdout.write('  Recently completed:')
            for pt in completed_tasks.order_by('-completed_at')[:3]:
                self.stdout.write(
                    f'    {pt.task.name} on {pt.completed_at}'
                )

        self.stdout.write(
            self.style.SUCCESS('=== End of Player Information ===')
        )