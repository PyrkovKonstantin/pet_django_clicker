from django.core.management.base import BaseCommand
from clicker_app.models import Task, PlayerTask


class Command(BaseCommand):
    help = 'Show detailed information about a task'

    def add_arguments(self, parser):
        parser.add_argument('task_id', type=int, help='ID of the task')

    def handle(self, *args, **options):
        task_id = options['task_id']
        
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Task with ID {task_id} does not exist!')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'=== Task Information: {task.name} ===')
        )

        # Basic task info
        self.stdout.write(f'ID: {task.id}')
        self.stdout.write(f'Description: {task.description}')
        self.stdout.write(f'Type: {task.task_type}')
        self.stdout.write(f'Target Value: {task.target_value}')
        self.stdout.write(f'Reward Coins: {task.reward_coins}')
        self.stdout.write(f'Reward Energy: {task.reward_energy}')
        self.stdout.write(f'Order: {task.order}')
        self.stdout.write(f'Active: {"Yes" if task.is_active else "No"}')

        # Players who have completed this task
        self.stdout.write(f'\nPlayers who completed this task:')
        completed_tasks = PlayerTask.objects.filter(task=task, is_completed=True).order_by('-completed_at')
        if completed_tasks.exists():
            for pt in completed_tasks[:10]:  # Show top 10
                self.stdout.write(
                    f'  {pt.player.username} on {pt.completed_at}'
                )
            if completed_tasks.count() > 10:
                self.stdout.write(
                    f'  ... and {completed_tasks.count() - 10} more players'
                )
        else:
            self.stdout.write('  No players have completed this task')

        # Players who are working on this task
        self.stdout.write(f'\nPlayers working on this task:')
        in_progress_tasks = PlayerTask.objects.filter(task=task, is_completed=False).order_by('-progress')
        if in_progress_tasks.exists():
            for pt in in_progress_tasks[:10]:  # Show top 10
                progress_percent = (pt.progress / task.target_value) * 100
                self.stdout.write(
                    f'  {pt.player.username}: {pt.progress}/{task.target_value} ({progress_percent:.1f}%)'
                )
            if in_progress_tasks.count() > 10:
                self.stdout.write(
                    f'  ... and {in_progress_tasks.count() - 10} more players'
                )
        else:
            self.stdout.write('  No players are working on this task')

        self.stdout.write(
            self.style.SUCCESS('=== End of Task Information ===')
        )