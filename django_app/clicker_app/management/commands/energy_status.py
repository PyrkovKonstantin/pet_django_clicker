from django.core.management.base import BaseCommand
from django.db.models import F
from clicker_app.models import Player


class Command(BaseCommand):
    help = 'Show energy status of all players'

    def add_arguments(self, parser):
        parser.add_argument(
            '--low-energy',
            action='store_true',
            help='Show only players with low energy (< 10%)'
        )
        parser.add_argument(
            '--full-energy',
            action='store_true',
            help='Show only players with full energy'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit the number of players shown',
            default=50
        )

    def handle(self, *args, **options):
        low_energy = options['low_energy']
        full_energy = options['full_energy']
        limit = options['limit']

        self.stdout.write(
            self.style.SUCCESS('=== Player Energy Status ===')
        )

        # Get players based on filter options
        players = Player.objects.all()
        
        if low_energy:
            players = players.filter(energy__lt=F('max_energy') * 0.1)
            self.stdout.write('Filter: Low Energy (< 10% of max)')
        elif full_energy:
            players = players.filter(energy=F('max_energy'))
            self.stdout.write('Filter: Full Energy')
        else:
            self.stdout.write('Showing all players')

        players = players.order_by('-energy')[:limit]

        if not players.exists():
            self.stdout.write('No players found matching criteria.')
            return

        # Header
        self.stdout.write(
            f"{'Username':<15} {'Energy':<15} {'Regen Rate':<12} {'Status':<15}"
        )
        self.stdout.write('-' * 65)

        # Player data
        for player in players:
            energy_percent = (player.energy / player.max_energy) * 100
            status = self.get_energy_status(energy_percent)
            
            self.stdout.write(
                f"{player.username:<15} "
                f"{player.energy}/{player.max_energy:<10} "
                f"{player.energy_regen_rate:<12} "
                f"{status:<15}"
            )

        self.stdout.write(
            self.style.SUCCESS(f'=== End of Energy Status (Showing {players.count()} players) ===')
        )

    def get_energy_status(self, energy_percent):
        """Return a status string based on energy percentage"""
        if energy_percent >= 90:
            return "Full"
        elif energy_percent >= 50:
            return "Good"
        elif energy_percent >= 25:
            return "Medium"
        elif energy_percent >= 10:
            return "Low"
        else:
            return "Critical"