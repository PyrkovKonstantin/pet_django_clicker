from django.core.management.base import BaseCommand
from clicker_app.models import Task


class Command(BaseCommand):
    help = 'Create sample tasks for the clicker game'

    def handle(self, *args, **options):
        # Create sample tasks
        tasks_data = [
            {
                'name': 'First Clicks',
                'description': 'Make 10 clicks',
                'task_type': 'clicks',
                'target_value': 10,
                'reward_coins': 50,
                'reward_energy': 0,
                'is_active': True,
                'order': 1
            },
            {
                'name': 'Upgrade Enthusiast',
                'description': 'Purchase 3 upgrades',
                'task_type': 'upgrades',
                'target_value': 3,
                'reward_coins': 100,
                'reward_energy': 50,
                'is_active': True,
                'order': 2
            },
            {
                'name': 'Level Up',
                'description': 'Reach level 5',
                'task_type': 'level',
                'target_value': 5,
                'reward_coins': 200,
                'reward_energy': 100,
                'is_active': True,
                'order': 3
            },
            {
                'name': 'Energy Master',
                'description': 'Reach level 10',
                'task_type': 'level',
                'target_value': 10,
                'reward_coins': 500,
                'reward_energy': 200,
                'is_active': True,
                'order': 4
            },
            {
                'name': 'Wealth Builder',
                'description': 'Accumulate 10,000 coins',
                'task_type': 'balance',
                'target_value': 10000,
                'reward_coins': 1000,
                'reward_energy': 100,
                'is_active': True,
                'order': 5
            }
        ]

        created_count = 0
        for task_data in tasks_data:
            task, created = Task.objects.get_or_create(
                name=task_data['name'],
                defaults=task_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created task: {task.name}')
                )
            else:
                self.stdout.write(
                    f'Task already exists: {task.name}'
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} tasks')
        )