from django.db import models
from django.utils import timezone
from phone_field import PhoneField 
# Create your models here.

class VaccinatedPerson(models.Model):

    GENDER_CHOICES = (('M','Male'),('F','Female'))

    name = models.CharField(verbose_name='Name',max_length=100,help_text=('Name of the Vaccinated Person'))
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth')
    phone_no = PhoneField(help_text=("Contact phone number"))
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        return timezone.now().year - self.dob.year

    def __str__(self):
        return self.name    