from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.VaccinatedPerson)

admin.site.register(models.Centre)