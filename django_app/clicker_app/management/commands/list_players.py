from django.core.management.base import BaseCommand
from clicker_app.models import Player


class Command(BaseCommand):
    help = 'List all players and their stats'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Listing all players...')
        )

        players = Player.objects.all().order_by('-balance')
        
        if not players.exists():
            self.stdout.write('No players found.')
            return

        # Header
        self.stdout.write(
            f"{'Username':<15} {'Balance':<10} {'Level':<6} {'Energy':<10} {'Clicks':<8}"
        )
        self.stdout.write('-' * 60)

        # Player data
        for player in players:
            self.stdout.write(
                f"{player.username:<15} "
                f"{player.balance:<10} "
                f"{player.level:<6} "
                f"{player.energy}/{player.max_energy:<10} "
                f"{player.coins_per_click:<8}"
            )

        self.stdout.write(
            self.style.SUCCESS(f'Total players: {players.count()}')
        )