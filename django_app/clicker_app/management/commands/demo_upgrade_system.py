from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clicker_app.models import Player, Upgrade, PlayerUpgrade


class Command(BaseCommand):
    help = 'Demonstrate the upgrade system'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Demonstrating upgrade system...')
        )

        # Create a test user and player if they don't exist
        user, created = User.objects.get_or_create(
            username='test_player2',
            defaults={'password': 'testpass123'}
        )
        
        player, created = Player.objects.get_or_create(
            user=user,
            defaults={
                'username': 'test_player2',
                'balance': 10000,
                'level': 5,
                'energy': 1000,
                'max_energy': 1000,
                'energy_regen_rate': 1,
                'coins_per_click': 1
            }
        )

        # Create a test upgrade if it doesn't exist
        upgrade, created = Upgrade.objects.get_or_create(
            name='Better Clicks',
            defaults={
                'description': 'Increase coins per click',
                'base_cost': 100,
                'cost_multiplier': 1.15,
                'upgrade_type': 'coins_per_click',
                'base_effect_value': 1,
                'effect_per_level': 1,
                'max_level': 10,
                'is_active': True
            }
        )

        self.stdout.write(f'Initial player state:')
        self.stdout.write(f'  Balance: {player.balance}')
        self.stdout.write(f'  Coins per click: {player.coins_per_click}')

        self.stdout.write(f'\nUpgrade info:')
        self.stdout.write(f'  Name: {upgrade.name}')
        self.stdout.write(f'  Base cost: {upgrade.base_cost}')
        self.stdout.write(f'  Cost multiplier: {upgrade.cost_multiplier}')

        # Check if player already has this upgrade
        player_upgrade, created = PlayerUpgrade.objects.get_or_create(
            player=player,
            upgrade=upgrade,
            defaults={'level': 0}
        )

        self.stdout.write(f'\nPlayer upgrade level: {player_upgrade.level}')

        # Calculate cost for next level
        next_level_cost = upgrade.get_cost(player_upgrade.level)
        self.stdout.write(f'Cost to upgrade to level {player_upgrade.level + 1}: {next_level_cost}')

        # Simulate purchasing the upgrade
        if player.balance >= next_level_cost:
            player.balance -= next_level_cost
            player_upgrade.level += 1
            player_upgrade.save()
            player.save()
            
            # Apply upgrade effect
            if upgrade.upgrade_type == 'coins_per_click':
                player.coins_per_click += upgrade.base_effect_value + (upgrade.effect_per_level * (player_upgrade.level - 1))
                player.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully upgraded to level {player_upgrade.level}!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('Not enough coins to purchase upgrade!')
            )

        self.stdout.write(f'\nUpdated player state:')
        self.stdout.write(f'  Balance: {player.balance}')
        self.stdout.write(f'  Coins per click: {player.coins_per_click}')
        self.stdout.write(f'  Upgrade level: {player_upgrade.level}')

        self.stdout.write(
            self.style.SUCCESS('Upgrade system demonstration complete!')
        )