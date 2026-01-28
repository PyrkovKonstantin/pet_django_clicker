from django.core.management.base import BaseCommand
from django.core import management
import os


class Command(BaseCommand):
    help = 'Restore game data from a backup file'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Path to the backup file to restore'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm restoration (required)'
        )

    def handle(self, *args, **options):
        backup_file = options['backup_file']
        confirm = options['confirm']

        if not confirm:
            self.stdout.write(
                self.style.WARNING('WARNING: This will overwrite existing game data!')
            )
            self.stdout.write(
                'Use --confirm to actually restore data.'
            )
            return

        # Check if backup file exists
        if not os.path.exists(backup_file):
            self.stdout.write(
                self.style.ERROR(f'Backup file not found: {backup_file}')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'Restoring game data from {backup_file}...')
        )

        try:
            # Load backup data
            management.call_command(
                'loaddata',
                backup_file,
                verbosity=2
            )
            
            self.stdout.write(
                self.style.SUCCESS('Successfully restored game data!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during restoration: {e}')
            )