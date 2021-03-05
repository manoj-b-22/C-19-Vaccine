from django.db import models
from django.utils import timezone
from phone_field import PhoneField 
# Create your models here.

class VaccinatedPerson(models.Model):

    GENDER_CHOICES = (('M','Male'),('F','Female'))

    name = models.CharField(verbose_name='Name',max_length=50,help_text=('Name of the Vaccinated Person'))
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth')
    phone_no = PhoneField(help_text=("Contact phone number"))
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        return timezone.now().year - self.dob.year

    def __str__(self):
        return self.name    


class Centres(models.Model):
    name = models.CharField(verbose_name="Name",max_length=50,help_text=('Name of the Vaccination Centre'))
    phone_no = PhoneField(help_text=('Contact number'))
    #address = 
    active_time_from = models.TimeField(help_text=('Active From'))
    active_time_to = models.TimeField(help_text=('To'))

    def __str__(self):
        return self.name
    
class Address(models.Model):
    address = models.TextField(max_length=128,help_text=('Address'))
    city = models.CharField(max_length=10,help_text=('City'))
    state = models.CharField(max_length=10,help_text=('State'))
    pincode = models.CharField(max_length=6,help_text=('Pincode'))
