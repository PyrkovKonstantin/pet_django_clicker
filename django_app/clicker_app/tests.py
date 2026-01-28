from django.test import TestCase
from django.contrib.auth.models import User
from .models import Player, Upgrade, PlayerUpgrade


class PlayerModelTest(TestCase):
    def setUp(self):
        # Create a user and player for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.player = Player.objects.create(
            user=self.user,
            username='testplayer',
            balance=1000,
            level=1,
            energy=100,
            max_energy=1000,
            energy_regen_rate=1,
            coins_per_click=1
        )

    def test_player_creation(self):
        """Test that a player is created correctly"""
        self.assertEqual(self.player.username, 'testplayer')
        self.assertEqual(self.player.balance, 1000)
        self.assertEqual(self.player.level, 1)
        self.assertEqual(self.player.energy, 100)
        self.assertEqual(self.player.max_energy, 1000)
        self.assertEqual(self.player.energy_regen_rate, 1)
        self.assertEqual(self.player.coins_per_click, 1)

    def test_player_string_representation(self):
        """Test the string representation of a player"""
        self.assertEqual(str(self.player), 'testplayer (Level 1)')


class UpgradeModelTest(TestCase):
    def setUp(self):
        # Create an upgrade for testing
        self.upgrade = Upgrade.objects.create(
            name='Test Upgrade',
            description='A test upgrade',
            base_cost=100,
            cost_multiplier=1.15,
            upgrade_type='coins_per_click',
            base_effect_value=1,
            effect_per_level=1,
            max_level=10
        )

    def test_upgrade_creation(self):
        """Test that an upgrade is created correctly"""
        self.assertEqual(self.upgrade.name, 'Test Upgrade')
        self.assertEqual(self.upgrade.base_cost, 100)
        self.assertEqual(self.upgrade.cost_multiplier, 1.15)
        self.assertEqual(self.upgrade.upgrade_type, 'coins_per_click')
        self.assertEqual(self.upgrade.base_effect_value, 1)
        self.assertEqual(self.upgrade.effect_per_level, 1)
        self.assertEqual(self.upgrade.max_level, 10)

    def test_upgrade_cost_calculation(self):
        """Test the cost calculation for upgrades"""
        # Cost at level 0 should be base_cost
        self.assertEqual(self.upgrade.get_cost(0), 100)
        
        # Cost at level 1 should be base_cost * cost_multiplier
        self.assertEqual(self.upgrade.get_cost(1), int(100 * 1.15))
        
        # Cost at level 2 should be base_cost * (cost_multiplier^2)
        self.assertEqual(self.upgrade.get_cost(2), int(100 * (1.15 ** 2)))
        
        # Cost should be None at max_level
        self.assertIsNone(self.upgrade.get_cost(10))

    def test_upgrade_string_representation(self):
        """Test the string representation of an upgrade"""
        self.assertEqual(str(self.upgrade), 'Test Upgrade')


class PlayerUpgradeModelTest(TestCase):
    def setUp(self):
        # Create a user, player, and upgrade for testing
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        self.player = Player.objects.create(
            user=self.user,
            username='testplayer2'
        )
        self.upgrade = Upgrade.objects.create(
            name='Test Upgrade 2',
            base_cost=50,
            cost_multiplier=1.2,
            upgrade_type='max_energy',
            base_effect_value=10,
            effect_per_level=10
        )
        self.player_upgrade = PlayerUpgrade.objects.create(
            player=self.player,
            upgrade=self.upgrade,
            level=3
        )

    def test_player_upgrade_creation(self):
        """Test that a player upgrade is created correctly"""
        self.assertEqual(self.player_upgrade.player, self.player)
        self.assertEqual(self.player_upgrade.upgrade, self.upgrade)
        self.assertEqual(self.player_upgrade.level, 3)

    def test_player_upgrade_string_representation(self):
        """Test the string representation of a player upgrade"""
        expected = 'testplayer2 - Test Upgrade 2 (Level 3)'
        self.assertEqual(str(self.player_upgrade), expected)
