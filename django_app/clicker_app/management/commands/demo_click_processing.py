from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clicker_app.models import Player
from django.utils import timezone


class Command(BaseCommand):
    help = 'Demonstrate the click processing system'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Demonstrating click processing system...')
        )

        # Create a test user and player if they don't exist
        user, created = User.objects.get_or_create(
            username='test_player3',
            defaults={'password': 'testpass123'}
        )
        
        player, created = Player.objects.get_or_create(
            user=user,
            defaults={
                'username': 'test_player3',
                'balance': 1000,
                'level': 1,
                'energy': 1000,
                'max_energy': 1000,
                'energy_regen_rate': 1,
                'coins_per_click': 1
            }
        )

        self.stdout.write(f'Initial player state:')
        self.stdout.write(f'  Balance: {player.balance}')
        self.stdout.write(f'  Energy: {player.energy}/{player.max_energy}')
        self.stdout.write(f'  Coins per click: {player.coins_per_click}')

        # Simulate processing clicks
        clicks = 10
        self.stdout.write(f'\nProcessing {clicks} clicks...')

        # Check if player has enough energy
        if player.energy >= clicks:
            # Process clicks
            player.energy -= clicks
            player.balance += clicks * player.coins_per_click
            player.last_energy_update = timezone.now()
            player.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully processed {clicks} clicks!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('Not enough energy to process clicks!')
            )

        self.stdout.write(f'\nUpdated player state:')
        self.stdout.write(f'  Balance: {player.balance}')
        self.stdout.write(f'  Energy: {player.energy}/{player.max_energy}')

        self.stdout.write(
            self.style.SUCCESS('Click processing demonstration complete!')
        )