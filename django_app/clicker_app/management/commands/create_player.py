from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clicker_app.models import Player


class Command(BaseCommand):
    help = 'Create a new player for testing'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new player')
        parser.add_argument('--password', type=str, help='Password for the new user', default='testpass123')
        parser.add_argument('--balance', type=int, help='Initial balance', default=1000)
        parser.add_argument('--energy', type=int, help='Initial energy', default=1000)

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        balance = options['balance']
        energy = options['energy']
        
        # Create Django user
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={'password': password}
        )
        
        if user_created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created Django user: {username}')
            )
        else:
            self.stdout.write(
                f'Django user already exists: {username}'
            )

        # Create player profile
        player, player_created = Player.objects.get_or_create(
            user=user,
            defaults={
                'username': username,
                'balance': balance,
                'level': 1,
                'energy': energy,
                'max_energy': 1000,
                'energy_regen_rate': 1,
                'coins_per_click': 1
            }
        )

        if player_created:
            self.stdout.write(
                self.style.SUCCESS(f'Created player profile: {username}')
            )
        else:
            self.stdout.write(
                f'Player profile already exists: {username}'
            )

        self.stdout.write(
            f'Player stats: Balance={player.balance}, Energy={player.energy}/{player.max_energy}'
        )