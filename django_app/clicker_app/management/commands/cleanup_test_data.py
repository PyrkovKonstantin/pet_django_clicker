from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clicker_app.models import Player, PlayerUpgrade, PlayerDailyReward, PlayerTask, Referral


class Command(BaseCommand):
    help = 'Clean up test data (USE WITH CAUTION!)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm', 
            action='store_true', 
            help='Confirm deletion of test data'
        )
        parser.add_argument(
            '--test-users-only', 
            action='store_true', 
            help='Only delete users with "test" in their username'
        )

    def handle(self, *args, **options):
        confirm = options['confirm']
        test_users_only = options['test_users_only']
        
        if not confirm:
            self.stdout.write(
                self.style.WARNING('WARNING: This will delete game data!')
            )
            self.stdout.write(
                'Use --confirm to actually delete data.'
            )
            return

        if test_users_only:
            # Only delete test users and their related data
            users = User.objects.filter(username__icontains='test')
            self.stdout.write(
                f'Deleting {users.count()} test users and related data...'
            )
        else:
            # Delete all game-related data
            users = User.objects.all()
            self.stdout.write(
                f'Deleting ALL {users.count()} users and related data...'
            )
            self.stdout.write(
                self.style.WARNING('THIS WILL DELETE ALL PLAYER DATA!')
            )

        # Delete related game data first
        if test_users_only:
            players = Player.objects.filter(user__in=users)
        else:
            players = Player.objects.all()
            
        deleted_upgrades = PlayerUpgrade.objects.filter(player__in=players).delete()
        deleted_rewards = PlayerDailyReward.objects.filter(player__in=players).delete()
        deleted_tasks = PlayerTask.objects.filter(player__in=players).delete()
        deleted_referrals = Referral.objects.filter(
            referrer__in=players
        ).delete()
        deleted_referrals2 = Referral.objects.filter(
            referred__in=players
        ).delete()
        
        # Delete players
        deleted_players = players.delete()
        
        # Delete users if requested
        if test_users_only:
            deleted_users = users.delete()
        
        self.stdout.write(
            self.style.SUCCESS('Cleanup completed successfully!')
        )
        self.stdout.write(
            f'Deleted {deleted_upgrades[0] if deleted_upgrades else 0} player upgrades'
        )
        self.stdout.write(
            f'Deleted {deleted_rewards[0] if deleted_rewards else 0} player rewards'
        )
        self.stdout.write(
            f'Deleted {deleted_tasks[0] if deleted_tasks else 0} player tasks'
        )
        self.stdout.write(
            f'Deleted {deleted_referrals[0] if deleted_referrals else 0} referrals'
        )
        self.stdout.write(
            f'Deleted {deleted_players[0] if deleted_players else 0} players'
        )
        if test_users_only:
            self.stdout.write(
                f'Deleted {deleted_users[0] if deleted_users else 0} users'
            )