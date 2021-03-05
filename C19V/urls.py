from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('VaccinationCentres',views.centres,name='centres'),
    path('create_person',views.createPerson,name="create_person"),
]