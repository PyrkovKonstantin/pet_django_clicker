from django.core.management.base import BaseCommand
from django.conf import settings
from clicker_app.models import Upgrade, DailyReward, Task


class Command(BaseCommand):
    help = 'Show current game configuration'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Clicker Game Configuration ===')
        )

        # Show Celery configuration
        self.stdout.write('\nCelery Configuration:')
        self.stdout.write(f'  Broker URL: {getattr(settings, "CELERY_BROKER_URL", "Not set")}')
        self.stdout.write(f'  Result Backend: {getattr(settings, "CELERY_RESULT_BACKEND", "Not set")}')
        self.stdout.write(f'  Timezone: {getattr(settings, "CELERY_TIMEZONE", "Not set")}')

        # Show database configuration
        self.stdout.write('\nDatabase Configuration:')
        db_config = getattr(settings, 'DATABASES', {}).get('default', {})
        self.stdout.write(f'  Engine: {db_config.get("ENGINE", "Not set")}')
        self.stdout.write(f'  Name: {db_config.get("NAME", "Not set")}')
        self.stdout.write(f'  Host: {db_config.get("HOST", "Not set")}')
        self.stdout.write(f'  Port: {db_config.get("PORT", "Not set")}')

        # Show upgrade configuration
        self.stdout.write('\nUpgrade Configuration:')
        upgrades = Upgrade.objects.filter(is_active=True).order_by('order')
        for upgrade in upgrades:
            self.stdout.write(
                f'  {upgrade.name}: '
                f'Base Cost={upgrade.base_cost}, '
                f'Type={upgrade.upgrade_type}, '
                f'Max Level={upgrade.max_level}'
            )

        # Show daily reward configuration
        self.stdout.write('\nDaily Reward Configuration:')
        rewards = DailyReward.objects.all().order_by('day')
        for reward in rewards:
            self.stdout.write(
                f'  Day {reward.day}: '
                f'{reward.reward_amount} {reward.reward_type}'
                f'{" (Special)" if reward.is_special else ""}'
            )

        # Show task configuration
        self.stdout.write('\nTask Configuration:')
        tasks = Task.objects.filter(is_active=True).order_by('order')
        for task in tasks:
            self.stdout.write(
                f'  {task.name}: '
                f'Type={task.task_type}, '
                f'Target={task.target_value}, '
                f'Reward={task.reward_coins} coins'
            )

        self.stdout.write(
            self.style.SUCCESS('\n=== End of Configuration ===')
        )