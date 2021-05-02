from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

# Signals for django User
# There are two types of Users. They differ in is_staff attribute.
# is_staff = true for TestCentre 
# is_staff = false for VaccinatedPerson

# Creating a instance of a User related model
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        models.VaccinatedPerson.objects.create(user=instance)
    if created and  instance.is_staff:
        models.TestCentre.objects.create(user=instance)

# Saving an instance of a created User related model
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_staff:
        instance.vaccinatedperson.save()
    if instance.is_staff:
        instance.testcentre.save()
