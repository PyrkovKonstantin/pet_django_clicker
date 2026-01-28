from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Set up all sample data for the clicker game'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Setting up sample data for the clicker game...')
        )

        # Create sample upgrades
        self.stdout.write('Creating sample upgrades...')
        call_command('create_sample_upgrades', verbosity=0)
        
        # Create sample daily rewards
        self.stdout.write('Creating sample daily rewards...')
        call_command('create_sample_rewards', verbosity=0)
        
        # Create sample tasks
        self.stdout.write('Creating sample tasks...')
        call_command('create_sample_tasks', verbosity=0)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up all sample data!')
        )