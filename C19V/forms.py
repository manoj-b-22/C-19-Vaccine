from . import models
from django import forms
from django.forms import ModelForm

class PersonForm(ModelForm):
    class Meta:
        model = models.VaccinatedPerson
        fields='__all__'
        labels={
            'dob':('Date of Birth'),
        }
        widgets={
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }