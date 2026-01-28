from django.apps import AppConfig


class ClickerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clicker_app'

    def ready(self):
        import clicker_app.signals  # noqa
