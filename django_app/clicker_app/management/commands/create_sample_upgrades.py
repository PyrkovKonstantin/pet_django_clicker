from django.core.management.base import BaseCommand
from clicker_app.models import Upgrade


class Command(BaseCommand):
    help = 'Create sample upgrades for the clicker game'

    def handle(self, *args, **options):
        # Create sample upgrades
        upgrades_data = [
            {
                'name': 'Better Clicks',
                'description': 'Increase coins per click',
                'icon': 'click_icon.png',
                'base_cost': 100,
                'cost_multiplier': 1.15,
                'upgrade_type': 'coins_per_click',
                'base_effect_value': 1,
                'effect_per_level': 1,
                'max_level': 50,
                'is_active': True,
                'order': 1
            },
            {
                'name': 'Energy Boost',
                'description': 'Increase maximum energy',
                'icon': 'energy_icon.png',
                'base_cost': 50,
                'cost_multiplier': 1.2,
                'upgrade_type': 'max_energy',
                'base_effect_value': 10,
                'effect_per_level': 10,
                'max_level': 30,
                'is_active': True,
                'order': 2
            },
            {
                'name': 'Fast Recharge',
                'description': 'Increase energy regeneration rate',
                'icon': 'regen_icon.png',
                'base_cost': 200,
                'cost_multiplier': 1.25,
                'upgrade_type': 'energy_regen',
                'base_effect_value': 1,
                'effect_per_level': 1,
                'max_level': 20,
                'is_active': True,
                'order': 3
            }
        ]

        created_count = 0
        for upgrade_data in upgrades_data:
            upgrade, created = Upgrade.objects.get_or_create(
                name=upgrade_data['name'],
                defaults=upgrade_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created upgrade: {upgrade.name}')
                )
            else:
                self.stdout.write(
                    f'Upgrade already exists: {upgrade.name}'
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} upgrades')
        )