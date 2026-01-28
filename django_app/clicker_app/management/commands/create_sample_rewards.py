from django.core.management.base import BaseCommand
from clicker_app.models import DailyReward


class Command(BaseCommand):
    help = 'Create sample daily rewards for the clicker game'

    def handle(self, *args, **options):
        # Create sample daily rewards
        rewards_data = [
            {'day': 1, 'reward_type': 'coins', 'reward_amount': 100, 'is_special': False},
            {'day': 2, 'reward_type': 'coins', 'reward_amount': 200, 'is_special': False},
            {'day': 3, 'reward_type': 'coins', 'reward_amount': 300, 'is_special': False},
            {'day': 4, 'reward_type': 'coins', 'reward_amount': 400, 'is_special': False},
            {'day': 5, 'reward_type': 'coins', 'reward_amount': 500, 'is_special': False},
            {'day': 6, 'reward_type': 'coins', 'reward_amount': 600, 'is_special': False},
            {'day': 7, 'reward_type': 'coins', 'reward_amount': 1000, 'is_special': True},
            {'day': 8, 'reward_type': 'coins', 'reward_amount': 800, 'is_special': False},
            {'day': 9, 'reward_type': 'coins', 'reward_amount': 900, 'is_special': False},
            {'day': 10, 'reward_type': 'coins', 'reward_amount': 2000, 'is_special': True},
        ]

        created_count = 0
        for reward_data in rewards_data:
            reward, created = DailyReward.objects.get_or_create(
                day=reward_data['day'],
                defaults=reward_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created reward for day {reward.day}')
                )
            else:
                self.stdout.write(
                    f'Reward for day {reward.day} already exists'
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} daily rewards')
        )