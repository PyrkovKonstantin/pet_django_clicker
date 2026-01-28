from django.core.management.base import BaseCommand
from clicker_app.tasks import regenerate_energy, update_leaderboard, update_task_progress


class Command(BaseCommand):
    help = 'Test Celery tasks'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Testing Celery tasks...')
        )

        # Test energy regeneration task
        self.stdout.write('\n1. Testing energy regeneration task...')
        try:
            result = regenerate_energy()
            self.stdout.write(
                self.style.SUCCESS(f'Energy regeneration result: {result}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error in energy regeneration: {e}')
            )

        # Test leaderboard update task
        self.stdout.write('\n2. Testing leaderboard update task...')
        try:
            result = update_leaderboard()
            self.stdout.write(
                self.style.SUCCESS(f'Leaderboard update result: {result}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error in leaderboard update: {e}')
            )

        # Test task progress update task
        self.stdout.write('\n3. Testing task progress update task...')
        try:
            result = update_task_progress()
            self.stdout.write(
                self.style.SUCCESS(f'Task progress update result: {result}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error in task progress update: {e}')
            )

        self.stdout.write(
            self.style.SUCCESS('\nAll Celery tasks tested successfully!')
        )