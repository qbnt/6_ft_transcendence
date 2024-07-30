# user_manage/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Profile

@receiver(post_delete, sender=Profile)
def delete_user_with_profile(sender, instance, **kwargs):
    user = instance.user
    if user and user.id:
        user.delete()