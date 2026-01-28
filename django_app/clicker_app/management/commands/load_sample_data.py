from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Load sample data for the clicker game'

    def handle(self, *args, **options):
        # Get the path to the fixture file
        fixture_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 
            'fixtures', 
            'sample_data.json'
        )
        
        # Load the fixture
        call_command('loaddata', fixture_path, verbosity=2)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data')
        )