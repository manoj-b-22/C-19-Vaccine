from . import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.admin import widgets

# Form for VaccinatedPerson model
class PersonForm(ModelForm):
    class Meta:
        model = models.VaccinatedPerson
        fields='__all__'
        labels={
            'dob':('Date of Birth'),
            'phone_no':('Phone Number'),
            'centre':('Vaccination Centre')
        }
        widgets={
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

# Form for TestCentre model
class TestCentreForm(ModelForm):
    class Meta:
        model = models.TestCentre
        fields='__all__'
        labels={
            'phone_no':('Phone Number'),
            'email':('Email ID'),
            'active_time_from':('Active From'),
            'active_time_to':('Active Till')
        }
        widgets={
            'active_time_from': widgets.AdminTimeWidget(),
            'active_time_to': widgets.AdminTimeWidget(),
        }

# Form for Status model
class StatusForm(ModelForm):
    class Meta:
        model = models.Status
        fields='__all__'

# Form for FAQ model
class FAQForm(ModelForm):
    class Meta:
        model = models.FAQ
        fields='__all__'

# Form for User model
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username','password1','password2','is_staff']    
