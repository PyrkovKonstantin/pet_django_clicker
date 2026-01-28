from celery.schedules import crontab

# Celery Beat Schedule
CELERYBEAT_SCHEDULE = {
    'regenerate-energy': {
        'task': 'clicker_app.tasks.regenerate_energy',
        'schedule': 30.0,  # Every 30 seconds
    },
    'update-leaderboard': {
        'task': 'clicker_app.tasks.update_leaderboard',
        'schedule': 600.0,  # Every 10 minutes
    },
    'update-task-progress': {
        'task': 'clicker_app.tasks.update_task_progress',
        'schedule': 3600.0,  # Every hour
    },
}

# Timezone for the Celery beat scheduler
CELERY_TIMEZONE = 'UTC'