# Django Clicker Game Architecture (Hamster Combat Inspired)

## 1. Django Models Design

### Player Model
```python
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
    last_energy_update = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
```

### Upgrade Model
```python
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
```

### PlayerUpgrade Model
```python
class PlayerUpgrade(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    upgrade = models.ForeignKey(Upgrade, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    purchased_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('player', 'upgrade')
```

### DailyReward Model
```python
class DailyReward(models.Model):
    day = models.IntegerField(unique=True)  # Day 1, 2, 3, etc.
    reward_type = models.CharField(max_length=20, default='coins')
    reward_amount = models.IntegerField()
    is_special = models.BooleanField(default=False)  # Special rewards for milestones
    
    class Meta:
        ordering = ['day']
```

### PlayerDailyReward Model
```python
class PlayerDailyReward(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    reward = models.ForeignKey(DailyReward, on_delete=models.CASCADE)
    claimed_at = models.DateTimeField(auto_now_add=True)
    is_consecutive = models.BooleanField(default=True)  # Whether this is part of a streak
```

### Task Model
```python
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
```

### PlayerTask Model
```python
class PlayerTask(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('player', 'task')
```

### Referral Model
```python
class Referral(models.Model):
    referrer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='referrals')
    referred = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='referred_by')
    created_at = models.DateTimeField(auto_now_add=True)
    reward_claimed = models.BooleanField(default=False)
```

## 2. API Endpoints

### Authentication
- `POST /api/auth/telegram/` - Authenticate via Telegram
- `POST /api/auth/register/` - Register with email/password
- `POST /api/auth/login/` - Login with email/password
- `POST /api/auth/logout/` - Logout

### Player
- `GET /api/player/` - Get player profile
- `PUT /api/player/` - Update player profile
- `POST /api/player/sync/` - Sync client state with server

### Game Mechanics
- `POST /api/click/` - Process a click
- `GET /api/energy/` - Get current energy status

### Upgrades
- `GET /api/upgrades/` - List all available upgrades
- `POST /api/upgrades/purchase/` - Purchase an upgrade

### Daily Rewards
- `GET /api/daily-rewards/` - Get daily reward status
- `POST /api/daily-rewards/claim/` - Claim daily reward

### Tasks
- `GET /api/tasks/` - List all tasks with progress
- `POST /api/tasks/claim/` - Claim completed task reward

### Leaderboard
- `GET /api/leaderboard/` - Get top players

## 3. Energy Regeneration System

### Implementation Approach
1. **Client-side tracking**: Energy is tracked on the client for immediate feedback
2. **Server validation**: Server validates energy state during sync operations
3. **Background regeneration**: Celery task updates energy every second for active players
4. **Last update tracking**: Track when energy was last updated to calculate regeneration

### Formula
```
current_energy = min(
    max_energy,
    previous_energy + (seconds_since_last_update * energy_regen_rate)
)
```

### Background Task
```python
# Celery task running every 30 seconds
def regenerate_energy():
    # Get players who were active recently
    active_players = Player.objects.filter(
        last_energy_update__gte=timezone.now() - timedelta(minutes=10)
    )
    
    for player in active_players:
        # Calculate regenerated energy
        seconds_passed = (timezone.now() - player.last_energy_update).seconds
        energy_gained = seconds_passed * player.energy_regen_rate
        player.energy = min(player.max_energy, player.energy + energy_gained)
        player.last_energy_update = timezone.now()
        player.save()
```

## 4. Anti-Cheat and Validation Mechanisms

### Click Validation
1. **Rate limiting**: Limit clicks per second on server side
2. **Energy validation**: Ensure player has enough energy for clicks
3. **Timestamp validation**: Check that click timestamps are reasonable
4. **Sequence validation**: Ensure click sequence is logical

### Upgrade Validation
1. **Cost validation**: Verify player has enough coins
2. **Level validation**: Ensure upgrade level is valid
3. **Effect validation**: Verify upgrade effects match expected values

### Sync Validation
1. **State comparison**: Compare client state with server state
2. **Delta validation**: Validate changes made since last sync
3. **Anomaly detection**: Flag suspicious patterns

### Implementation
```python
def validate_click(player, click_data):
    # Check energy
    if player.energy < 1:
        raise ValidationError("Not enough energy")
    
    # Check rate limiting
    if click_data['timestamp'] - player.last_click_timestamp < 100:  # 100ms minimum
        raise ValidationError("Clicks too fast")
    
    # Check energy consumption
    expected_energy = player.energy - 1
    if click_data['energy'] != expected_energy:
        raise ValidationError("Energy mismatch")
    
    # Update player
    player.energy = expected_energy
    player.balance += player.coins_per_click
    player.last_click_timestamp = click_data['timestamp']
    player.save()
```

## 5. Optimization Strategies

### Caching
1. **Player data**: Cache player profile in Redis with 5-minute expiry
2. **Upgrade data**: Cache upgrade templates as they rarely change
3. **Leaderboard**: Cache top players with 10-minute expiry
4. **Daily rewards**: Cache reward data with 1-hour expiry

### Database Optimization
1. **Indexing**: Index frequently queried fields (player_id, upgrade_id, etc.)
2. **Bulk operations**: Use bulk_create/bulk_update for batch operations
3. **Query optimization**: Use select_related and prefetch_related

### Background Tasks
1. **Energy regeneration**: Celery task for energy regeneration
2. **Leaderboard calculation**: Periodic task to update leaderboards
3. **Daily reset**: Reset daily rewards at midnight
4. **Cleanup tasks**: Remove old data, archive inactive players

### Partial Updates
1. **Delta sync**: Only send changed data between client and server
2. **Batch operations**: Batch multiple operations in single requests
3. **WebSockets**: Use WebSockets for real-time updates where appropriate

## 6. Additional Features

### Leaderboard System
```python
# Calculate and cache top players
def update_leaderboard():
    top_players = Player.objects.order_by('-balance')[:100]
    cache.set('leaderboard', [
        {
            'id': p.id,
            'username': p.username,
            'balance': p.balance,
            'level': p.level
        } for p in top_players
    ], 600)  # Cache for 10 minutes
```

### Referral System
1. **Tracking**: Track referral relationships in database
2. **Rewards**: Award both referrer and referred player
3. **Validation**: Prevent self-referrals and duplicate referrals

### Telegram Mini App Integration
1. **InitData validation**: Verify Telegram initData signature
2. **User data extraction**: Extract user data from Telegram
3. **Deep linking**: Support referral links via Telegram

## 7. Deployment Considerations

### Scalability
1. **Database sharding**: Consider sharding for large player base
2. **Load balancing**: Use load balancer for multiple app instances
3. **Caching layer**: Implement Redis for caching
4. **CDN**: Use CDN for static assets

### Monitoring
1. **Performance metrics**: Track API response times
2. **Error tracking**: Monitor and alert on errors
3. **Business metrics**: Track player engagement and retention