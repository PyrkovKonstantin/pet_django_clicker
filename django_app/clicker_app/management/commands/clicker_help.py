from django.core.management.base import BaseCommand
from django.core.management import get_commands, load_command_class


class Command(BaseCommand):
    help = 'Show help information for clicker game commands'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Clicker Game Management Commands ===')
        )

        # List all clicker_app commands
        commands = get_commands()
        clicker_commands = {
            name: app for name, app in commands.items() 
            if app == 'clicker_app' and name.startswith('clicker_')
        }
        
        # Add commands without clicker_ prefix
        other_commands = {
            name: app for name, app in commands.items() 
            if app == 'clicker_app' and not name.startswith('clicker_')
        }
        
        all_commands = {**clicker_commands, **other_commands}

        if not all_commands:
            self.stdout.write('No clicker game commands found.')
            return

        for command_name in sorted(all_commands.keys()):
            try:
                command_class = load_command_class('clicker_app', command_name)
                help_text = getattr(command_class, 'help', 'No help available')
                self.stdout.write(f"\n{self.style.BOLD}{command_name}{self.style.ENDC}")
                self.stdout.write(f"  {help_text}")
            except Exception as e:
                self.stdout.write(f"\n{self.style.BOLD}{command_name}{self.style.ENDC}")
                self.stdout.write(f"  Error loading help: {e}")

        self.stdout.write(
            self.style.SUCCESS('\n=== End of Commands ===')
        )
        self.stdout.write(
            'Use "python manage.py <command> --help" for detailed help on each command.'
        )