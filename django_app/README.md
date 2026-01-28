# Django Clicker Game

A Django-based clicker game inspired by Hamster Combat, built with Django REST Framework.

## Features

- Player authentication and profiles
- Click-based gameplay with energy management
- Upgrade system with multiple enhancement types
- Daily rewards and task system
- Leaderboards and referral system
- Background task processing with Celery
- RESTful API for game interactions

## Technical Stack

- **Backend**: Django 6.0 + Django REST Framework
- **Database**: PostgreSQL
- **Caching**: Redis
- **Background Tasks**: Celery
- **Authentication**: Session-based

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database and update settings.py with your database credentials.

3. Set up Redis for caching and Celery:
   ```bash
   # Install Redis (Ubuntu/Debian)
   sudo apt-get install redis-server
   
   # Start Redis server
   sudo service redis-server start
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Start Celery worker (in a separate terminal):
   ```bash
   celery -A django_app worker -l info
   ```

8. Start Celery beat scheduler (in a separate terminal):
   ```bash
   celery -A django_app beat -l info
   ```

## API Endpoints

### Authentication
- `GET /api/player/` - Get player profile
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

## Project Structure

```
django_app/
├── clicker_app/          # Main game application
│   ├── models.py         # Data models
│   ├── views.py          # API views
│   ├── serializers.py   # Data serializers
│   ├── tasks.py          # Celery background tasks
│   ├── admin.py          # Admin interface configuration
│   ├── apps.py           # App configuration
│   ├── signals.py        # Django signals
│   └── migrations/      # Database migrations
├── django_app/           # Django project settings
│   ├── settings.py       # Project settings
│   ├── urls.py           # URL routing
│   ├── celery.py          # Celery configuration
│   └── __init__.py       # Package initialization
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Background Tasks

The game uses Celery for background task processing:

1. **Energy Regeneration**: Runs every 30 seconds to regenerate energy for active players
2. **Leaderboard Updates**: Periodically updates cached leaderboard data
3. **Task Progress Updates**: Updates player progress on various tasks

## Security Features

- Rate limiting for click actions
- Energy validation to prevent cheating
- Timestamp validation for actions
- Server-side validation of all game state changes

## Optimization Strategies

- Redis caching for frequently accessed data
- Database indexing for performance
- Background task processing for non-critical operations
- Partial updates to minimize data transfer