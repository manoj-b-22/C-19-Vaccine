from . import models
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets

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