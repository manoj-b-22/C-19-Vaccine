from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.VaccinatedPerson)

admin.site.register(models.TestCentre)

admin.site.register(models.Status)

admin.site.register(models.FAQ)