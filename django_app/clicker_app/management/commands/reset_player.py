from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clicker_app.models import Player, PlayerUpgrade, PlayerDailyReward, PlayerTask


class Command(BaseCommand):
    help = 'Reset a player\'s game state'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the player to reset')

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
            f'Resetting game state for player: {player.username}'
        )

        # Reset player stats
        player.balance = 0
        player.level = 1
        player.energy = 1000
        player.max_energy = 1000
        player.energy_regen_rate = 1
        player.coins_per_click = 1
        player.save()

        # Delete player upgrades
        PlayerUpgrade.objects.filter(player=player).delete()
        
        # Delete player daily rewards
        PlayerDailyReward.objects.filter(player=player).delete()
        
        # Reset player tasks
        PlayerTask.objects.filter(player=player).update(
            progress=0,
            is_completed=False,
            completed_at=None
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully reset game state for {username}!')
        )