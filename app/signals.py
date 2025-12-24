# app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Yangi User yaratilganda Profile ham yaratilishini ta'minlaydi.
    get_or_create ishlatilib, duplicate profil yaratilishi oldini oladi.
    """
    if created:
        Profile.objects.get_or_create(user=instance)