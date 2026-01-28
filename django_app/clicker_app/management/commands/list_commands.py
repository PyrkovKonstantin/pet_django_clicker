from django.core.management.base import BaseCommand
from django.core.management import get_commands


class Command(BaseCommand):
    help = 'List all available management commands'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Available Management Commands ===')
        )

        # Get all commands
        commands = get_commands()
        
        # Group commands by app
        app_commands = {}
        for command, app in commands.items():
            if app not in app_commands:
                app_commands[app] = []
            app_commands[app].append(command)
        
        # Show clicker_app commands first
        if 'clicker_app' in app_commands:
            self.stdout.write(f'\n{self.style.BOLD}Clicker App Commands:{self.style.ENDC}')
            for command in sorted(app_commands['clicker_app']):
                self.stdout.write(f'  {command}')
            del app_commands['clicker_app']
        
        # Show other app commands
        for app in sorted(app_commands.keys()):
            self.stdout.write(f'\n{self.style.BOLD}{app.title()} Commands:{self.style.ENDC}')
            for command in sorted(app_commands[app]):
                self.stdout.write(f'  {command}')

        self.stdout.write(
            self.style.SUCCESS('\n=== End of Commands ===')
        )
        self.stdout.write(
            'Use "python manage.py <command> --help" for detailed help on each command.'
        )