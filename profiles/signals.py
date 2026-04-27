from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from .models import EmployeeProfile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(user=instance)
