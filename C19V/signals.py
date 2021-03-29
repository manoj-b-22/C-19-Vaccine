from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not User.is_staff:
        models.VaccinatedPerson.objects.create(user=instance)
    if created and  User.is_staff:
        models.TestCentre.objects.create(user=instance)    

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not User.is_staff:
        instance.vaccinatedperson.save()
    if User.is_staff:
        instance.testcentre.save()
