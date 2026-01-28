from django.core.management.base import BaseCommand
from clicker_app.models import Referral


class Command(BaseCommand):
    help = 'Show referral information'

    def add_arguments(self, parser):
        parser.add_argument(
            '--player',
            type=str,
            help='Show referrals for a specific player',
            default=None
        )

    def handle(self, *args, **options):
        player_name = options['player']

        if player_name:
            self.stdout.write(
                self.style.SUCCESS(f'=== Referral Information for {player_name} ===')
            )
            
            # Show referrals made by this player
            referrals = Referral.objects.filter(referrer__username=player_name)
            self.stdout.write(f'\nPlayers referred by {player_name}:')
            if referrals.exists():
                for ref in referrals:
                    reward_status = "Claimed" if ref.reward_claimed else "Not claimed"
                    self.stdout.write(
                        f'  {ref.referred.username} - {reward_status}'
                    )
            else:
                self.stdout.write('  No referrals found')
                
            # Show who referred this player
            try:
                referral = Referral.objects.get(referred__username=player_name)
                reward_status = "Claimed" if referral.reward_claimed else "Not claimed"
                self.stdout.write(
                    f'\nReferred by: {referral.referrer.username} - {reward_status}'
                )
            except Referral.DoesNotExist:
                self.stdout.write(f'\n{player_name} was not referred by anyone')
        else:
            self.stdout.write(
                self.style.SUCCESS('=== Referral Information ===')
            )
            
            # Show all referrals
            referrals = Referral.objects.all().order_by('-created_at')
            if referrals.exists():
                self.stdout.write(f'\nRecent referrals:')
                for ref in referrals[:10]:  # Show top 10
                    reward_status = "Claimed" if ref.reward_claimed else "Not claimed"
                    self.stdout.write(
                        f'  {ref.referrer.username} -> {ref.referred.username} - {reward_status}'
                    )
                if referrals.count() > 10:
                    self.stdout.write(
                        f'  ... and {referrals.count() - 10} more referrals'
                    )
            else:
                self.stdout.write('\nNo referrals found')

        # Show statistics
        total_referrals = Referral.objects.count()
        claimed_rewards = Referral.objects.filter(reward_claimed=True).count()
        
        self.stdout.write(f'\nStatistics:')
        self.stdout.write(f'  Total referrals: {total_referrals}')
        self.stdout.write(f'  Claimed rewards: {claimed_rewards}')
        if total_referrals > 0:
            claim_rate = (claimed_rewards / total_referrals) * 100
            self.stdout.write(f'  Claim rate: {claim_rate:.2f}%')

        self.stdout.write(
            self.style.SUCCESS('=== End of Referral Information ===')
        )