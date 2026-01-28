from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run all demonstration scripts for the clicker game'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Running all demonstration scripts...')
        )

        # Run energy regeneration demo
        self.stdout.write('\n1. Running energy regeneration demo...')
        call_command('demo_energy_regeneration', verbosity=0)
        
        # Run upgrade system demo
        self.stdout.write('\n2. Running upgrade system demo...')
        call_command('demo_upgrade_system', verbosity=0)
        
        # Run click processing demo
        self.stdout.write('\n3. Running click processing demo...')
        call_command('demo_click_processing', verbosity=0)
        
        self.stdout.write(
            self.style.SUCCESS('All demonstrations completed successfully!')
        )