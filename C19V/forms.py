from . import models
from django.forms import ModelForm

class PersonForm(ModelForm):
    class Meta:
        model = models.VaccinatedPerson
        fields='__all__'