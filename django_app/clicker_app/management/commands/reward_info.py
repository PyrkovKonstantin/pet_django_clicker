from django.core.management.base import BaseCommand
from clicker_app.models import DailyReward, PlayerDailyReward


class Command(BaseCommand):
    help = 'Show detailed information about a daily reward'

    def add_arguments(self, parser):
        parser.add_argument('day', type=int, help='Day number of the reward')

    def handle(self, *args, **options):
        day = options['day']
        
        try:
            reward = DailyReward.objects.get(day=day)
        except DailyReward.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Daily reward for day {day} does not exist!')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'=== Daily Reward Information: Day {reward.day} ===')
        )

        # Basic reward info
        self.stdout.write(f'ID: {reward.id}')
        self.stdout.write(f'Reward Type: {reward.reward_type}')
        self.stdout.write(f'Reward Amount: {reward.reward_amount}')
        self.stdout.write(f'Special: {"Yes" if reward.is_special else "No"}')

        # Players who have claimed this reward
        self.stdout.write(f'\nPlayers who claimed this reward:')
        player_rewards = PlayerDailyReward.objects.filter(reward=reward).order_by('-claimed_at')
        if player_rewards.exists():
            for pr in player_rewards[:10]:  # Show top 10
                self.stdout.write(
                    f'  {pr.player.username} on {pr.claimed_at}'
                )
            if player_rewards.count() > 10:
                self.stdout.write(
                    f'  ... and {player_rewards.count() - 10} more players'
                )
        else:
            self.stdout.write('  No players have claimed this reward')

        # Show next few rewards for context
        self.stdout.write(f'\nNext few rewards:')
        next_rewards = DailyReward.objects.filter(day__gt=day).order_by('day')[:5]
        for nr in next_rewards:
            special = " (Special)" if nr.is_special else ""
            self.stdout.write(
                f'  Day {nr.day}: {nr.reward_amount} {nr.reward_type}{special}'
            )

        self.stdout.write(
            self.style.SUCCESS('=== End of Daily Reward Information ===')
        )