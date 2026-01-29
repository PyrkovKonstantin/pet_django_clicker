from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=150, blank=True)
    balance = models.BigIntegerField(default=0)
    level = models.IntegerField(default=1)
    energy = models.IntegerField(default=1000)
    max_energy = models.IntegerField(default=1000)
    energy_regen_rate = models.IntegerField(default=1)  # Energy regenerated per second
    coins_per_click = models.IntegerField(default=1)
    last_energy_update = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def get_current_energy(self):
        """
        Calculate current energy based on time passed since last update
        """
        if self.energy >= self.max_energy:
            return self.energy
        
        # Calculate seconds passed since last energy update
        time_passed = timezone.now() - self.last_energy_update
        seconds_passed = int(time_passed.total_seconds())
        
        # Calculate energy regenerated
        energy_regenerated = seconds_passed * self.energy_regen_rate
        
        # Update energy (but not above max_energy)
        new_energy = min(self.energy + energy_regenerated, self.max_energy)
        
        return new_energy

    def update_energy(self):
        """
        Update energy and last_energy_update timestamp
        """
        current_energy = self.get_current_energy()
        if current_energy != self.energy:
            self.energy = current_energy
            self.last_energy_update = timezone.now()
            self.save(update_fields=['energy', 'last_energy_update'])
        return self.energy

    def __str__(self):
        return f"{self.username or self.user.username} (Level {self.level})"


class Upgrade(models.Model):
    UPGRADE_TYPES = [
        ('coins_per_click', 'Coins Per Click'),
        ('max_energy', 'Max Energy'),
        ('energy_regen', 'Energy Regeneration'),
        ('multiplier', 'Coin Multiplier'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    base_cost = models.IntegerField()
    cost_multiplier = models.FloatField(default=1.15)  # Cost increases by this factor each level
    upgrade_type = models.CharField(max_length=20, choices=UPGRADE_TYPES)
    base_effect_value = models.IntegerField()  # Base value of the effect
    effect_per_level = models.IntegerField()  # Additional effect per level
    max_level = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)  # For UI ordering
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_cost(self, current_level):
        """Calculate the cost of upgrading to the next level"""
        if current_level >= self.max_level:
            return None  # Already at max level
        return int(self.base_cost * (self.cost_multiplier ** current_level))


class PlayerUpgrade(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    upgrade = models.ForeignKey(Upgrade, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    purchased_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('player', 'upgrade')

    def __str__(self):
        return f"{self.player.username} - {self.upgrade.name} (Level {self.level})"


class DailyReward(models.Model):
    day = models.IntegerField(unique=True)  # Day 1, 2, 3, etc.
    reward_type = models.CharField(max_length=20, default='coins')
    reward_amount = models.IntegerField()
    is_special = models.BooleanField(default=False)  # Special rewards for milestones
    
    class Meta:
        ordering = ['day']

    def __str__(self):
        return f"Day {self.day} Reward"


class PlayerDailyReward(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    reward = models.ForeignKey(DailyReward, on_delete=models.CASCADE)
    claimed_at = models.DateTimeField(default=timezone.now)
    is_consecutive = models.BooleanField(default=True)  # Whether this is part of a streak

    def __str__(self):
        return f"{self.player.username} - {self.reward}"


class Task(models.Model):
    TASK_TYPES = [
        ('clicks', 'Total Clicks'),
        ('upgrades', 'Upgrades Purchased'),
        ('referrals', 'Referrals'),
        ('level', 'Reach Level'),
        ('balance', 'Balance Target'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    target_value = models.IntegerField()
    reward_coins = models.IntegerField()
    reward_energy = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class PlayerTask(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('player', 'task')

    def __str__(self):
        return f"{self.player.username} - {self.task.name}"


class Referral(models.Model):
    referrer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='referrals')
    referred = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='referred_by')
    created_at = models.DateTimeField(default=timezone.now)
    reward_claimed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.referrer.username} referred {self.referred.username}"