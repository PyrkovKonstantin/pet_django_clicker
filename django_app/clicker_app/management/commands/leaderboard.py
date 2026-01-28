from django.core.management.base import BaseCommand
from clicker_app.models import Player


class Command(BaseCommand):
    help = 'Show current leaderboard'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Number of players to show (default: 10)',
            default=10
        )
        parser.add_argument(
            '--sort',
            type=str,
            help='Sort by: balance, level, or energy (default: balance)',
            default='balance'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        sort_by = options['sort']

        # Validate sort option
        valid_sorts = ['balance', 'level', 'energy']
        if sort_by not in valid_sorts:
            self.stdout.write(
                self.style.WARNING(f'Invalid sort option. Using "balance".')
            )
            sort_by = 'balance'

        self.stdout.write(
            self.style.SUCCESS(f'=== Leaderboard (Top {limit} players by {sort_by}) ===')
        )

        # Get players sorted by the specified field
        if sort_by == 'energy':
            players = Player.objects.order_by('-energy', '-balance')[:limit]
        else:
            players = Player.objects.order_by(f'-{sort_by}', '-balance')[:limit]

        if not players.exists():
            self.stdout.write('No players found.')
            return

        # Header
        self.stdout.write(
            f"{'Rank':<4} {'Username':<15} {'Balance':<12} {'Level':<6} {'Energy':<10}"
        )
        self.stdout.write('-' * 55)

        # Player data
        for i, player in enumerate(players, 1):
            self.stdout.write(
                f"{i:<4} "
                f"{player.username:<15} "
                f"{player.balance:<12} "
                f"{player.level:<6} "
                f"{player.energy}/{player.max_energy:<10}"
            )

        self.stdout.write(
            self.style.SUCCESS(f'=== End of Leaderboard ===')
        )