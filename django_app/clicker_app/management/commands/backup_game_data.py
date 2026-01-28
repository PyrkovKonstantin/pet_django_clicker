from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Backup game data to a fixture file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output', 
            type=str, 
            help='Output file path (default: backups/game_backup_YYYYMMDD_HHMMSS.json)',
            default=None
        )
        parser.add_argument(
            '--models', 
            type=str, 
            help='Comma-separated list of models to backup (default: all)',
            default=None
        )

    def handle(self, *args, **options):
        # Create backups directory if it doesn't exist
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            self.stdout.write(
                self.style.SUCCESS(f'Created backup directory: {backup_dir}')
            )

        # Determine output file path
        if options['output']:
            output_file = options['output']
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'{backup_dir}/game_backup_{timestamp}.json'

        # Determine models to backup
        if options['models']:
            models = options['models'].split(',')
            app_models = [f'clicker_app.{model.strip()}' for model in models]
        else:
            # Backup all clicker_app models
            app_models = [
                'clicker_app.Player',
                'clicker_app.Upgrade',
                'clicker_app.PlayerUpgrade',
                'clicker_app.DailyReward',
                'clicker_app.PlayerDailyReward',
                'clicker_app.Task',
                'clicker_app.PlayerTask',
                'clicker_app.Referral'
            ]

        self.stdout.write(
            self.style.SUCCESS(f'Backing up game data to {output_file}...')
        )

        try:
            # Create backup
            with open(output_file, 'w') as f:
                management.call_command(
                    'dumpdata', 
                    *app_models,
                    format='json',
                    indent=2,
                    stdout=f
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully backed up data to {output_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during backup: {e}')
            )