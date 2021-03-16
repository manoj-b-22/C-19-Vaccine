from django.db.models import fields
import django_filters
from django_filters import DateFilter,CharFilter

from . import models

class PersonFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created',lookup_expr='gte')
    end_date = DateFilter(field_name='date_created',lookup_expr='lte')
    city = CharFilter(field_name='city',lookup_expr='icontains')
    state = CharFilter(field_name='state',lookup_expr='icontains')

    class Meta:
        model=models.VaccinatedPerson
        fields='__all__'
        exclude=['name','dob','phone_no','date_created','address','centre']

class PatientFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',lookup_expr='icontains')
    class Meta:
        model=models.VaccinatedPerson
        fields=['name']       
        
