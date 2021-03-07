from django.db import models
from django.utils import timezone
# Create your models here.

class TestCentre(models.Model):
    name = models.CharField(verbose_name="Name",max_length=50)
    email = models.EmailField(max_length=25)
    phone_no =models.CharField(max_length=10)
    address = models.TextField(max_length=128)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    active_time_from = models.TimeField(help_text=('From'))
    active_time_to = models.TimeField(help_text=('To'))

    def __str__(self):
        return self.name
    

class VaccinatedPerson(models.Model):

    GENDER_CHOICES = (('M','Male'),('F','Female'))

    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    dob = models.DateField()
    phone_no =models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    centre = models.ForeignKey(TestCentre,on_delete=models.CASCADE)

    @property
    def age(self):
        return timezone.now().year - self.dob.year

    def __str__(self):
        return self.name    

class         
