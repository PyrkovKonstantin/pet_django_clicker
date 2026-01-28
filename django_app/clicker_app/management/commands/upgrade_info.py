from django.core.management.base import BaseCommand
from clicker_app.models import Upgrade, PlayerUpgrade


class Command(BaseCommand):
    help = 'Show detailed information about an upgrade'

    def add_arguments(self, parser):
        parser.add_argument('upgrade_id', type=int, help='ID of the upgrade')

    def handle(self, *args, **options):
        upgrade_id = options['upgrade_id']
        
        try:
            upgrade = Upgrade.objects.get(id=upgrade_id)
        except Upgrade.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Upgrade with ID {upgrade_id} does not exist!')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'=== Upgrade Information: {upgrade.name} ===')
        )

        # Basic upgrade info
        self.stdout.write(f'ID: {upgrade.id}')
        self.stdout.write(f'Description: {upgrade.description}')
        self.stdout.write(f'Type: {upgrade.upgrade_type}')
        self.stdout.write(f'Base Cost: {upgrade.base_cost}')
        self.stdout.write(f'Cost Multiplier: {upgrade.cost_multiplier}')
        self.stdout.write(f'Base Effect: {upgrade.base_effect_value}')
        self.stdout.write(f'Effect per Level: {upgrade.effect_per_level}')
        self.stdout.write(f'Max Level: {upgrade.max_level}')
        self.stdout.write(f'Order: {upgrade.order}')
        self.stdout.write(f'Active: {"Yes" if upgrade.is_active else "No"}')

        # Cost calculation for next few levels
        self.stdout.write(f'\nCost for next levels:')
        for level in range(0, min(5, upgrade.max_level)):
            cost = upgrade.get_cost(level)
            if cost is not None:
                self.stdout.write(f'  Level {level + 1}: {cost} coins')

        # Players who have purchased this upgrade
        self.stdout.write(f'\nPlayers with this upgrade:')
        player_upgrades = PlayerUpgrade.objects.filter(upgrade=upgrade).order_by('-level')
        if player_upgrades.exists():
            for pu in player_upgrades[:10]:  # Show top 10
                self.stdout.write(
                    f'  {pu.player.username}: Level {pu.level}'
                )
            if player_upgrades.count() > 10:
                self.stdout.write(
                    f'  ... and {player_upgrades.count() - 10} more players'
                )
        else:
            self.stdout.write('  No players have purchased this upgrade')

        self.stdout.write(
            self.style.SUCCESS('=== End of Upgrade Information ===')
        )