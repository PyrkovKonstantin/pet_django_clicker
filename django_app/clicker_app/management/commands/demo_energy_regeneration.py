from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clicker_app.models import Player
from clicker_app.tasks import regenerate_energy
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Demonstrate the energy regeneration system'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Demonstrating energy regeneration system...')
        )

        # Create a test user and player if they don't exist
        user, created = User.objects.get_or_create(
            username='test_player',
            defaults={'password': 'testpass123'}
        )
        
        player, created = Player.objects.get_or_create(
            user=user,
            defaults={
                'username': 'test_player',
                'balance': 1000,
                'level': 1,
                'energy': 100,
                'max_energy': 1000,
                'energy_regen_rate': 1,
                'coins_per_click': 1
            }
        )

        self.stdout.write(f'Initial player state:')
        self.stdout.write(f'  Energy: {player.energy}/{player.max_energy}')
        self.stdout.write(f'  Last update: {player.last_energy_update}')

        # Simulate time passing by manually updating last_energy_update
        player.last_energy_update = timezone.now() - timedelta(minutes=5)
        player.save()
        
        self.stdout.write(f'\nSimulated 5 minutes passing...')
        self.stdout.write(f'Last update set to: {player.last_energy_update}')

        # Run the energy regeneration task
        result = regenerate_energy()
        self.stdout.write(f'\nEnergy regeneration result: {result}')

        # Refresh player data
        player.refresh_from_db()
        
        self.stdout.write(f'\nUpdated player state:')
        self.stdout.write(f'  Energy: {player.energy}/{player.max_energy}')
        self.stdout.write(f'  Last update: {player.last_energy_update}')

        self.stdout.write(
            self.style.SUCCESS('Energy regeneration demonstration complete!')
        )