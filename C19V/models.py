from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class TestCentre(models.Model):
    user = models.OneToOneField(User,on_delete=CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=25)
    phone_no =models.CharField(max_length=10)
    address = models.TextField(max_length=128)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    active_time_from = models.TimeField() #From
    active_time_to = models.TimeField()   #To

    def __str__(self):
        return self.name
    

class VaccinatedPerson(models.Model):

    GENDER_CHOICES = (('M','Male'),('F','Female'))

    user = models.OneToOneField(User,on_delete=CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    dob = models.DateField()
    phone_no =models.CharField(max_length=10)
    address = models.TextField(max_length=128)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    centre = models.OneToOneField(TestCentre,on_delete=models.CASCADE)

    @property
    def age(self):
        return timezone.now().year - self.dob.year

    def __str__(self):
        return self.name    

class Status(models.Model):
    STATUS = (('Good','Feeling good'),('Ok','Feeling somewhat good'),('Bad','Feeling Bad'))

    status = models.CharField(max_length=4,choices=STATUS)
    person = models.ForeignKey(VaccinatedPerson,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.person.name+" "+self.status
