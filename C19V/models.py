from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class TestCentre(models.Model):
    user = models.OneToOneField(User,on_delete=CASCADE)
    name = models.CharField(max_length=50,null=True)
    email = models.EmailField(max_length=25,null=True)
    phone_no =models.CharField(max_length=10,null=True)
    address = models.TextField(max_length=128,null=True)
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    pincode = models.CharField(max_length=6,null=True)
    active_time_from = models.TimeField(null=True) #From
    active_time_to = models.TimeField(null=True)   #To

    def __str__(self):
        return self.name
    

class VaccinatedPerson(models.Model):

    GENDER_CHOICES = (('M','Male'),('F','Female'))

    user = models.OneToOneField(User,on_delete=CASCADE)
    name = models.CharField(max_length=50,null=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True)
    dob = models.DateField(null=True)
    phone_no =models.CharField(max_length=10,null=True)
    address = models.TextField(max_length=128,null=True)
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    centre = models.CharField(max_length=50,null=True)

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

class FAQ(models.Model):
    question = models.TextField(max_length=100)
    answer = models.TextField(max_length=500)
