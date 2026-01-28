from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Player


@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    """
    Create a player profile when a Django user is created
    """
    if created:
        Player.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_player_profile(sender, instance, **kwargs):
    """
    Save the player profile when the Django user is saved
    """
    try:
        instance.player.save()
    except Player.DoesNotExist:
        pass