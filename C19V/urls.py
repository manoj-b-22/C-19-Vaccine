from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('/HealthReport',views.health,name="health"),
    path('/Statistics',views.stats,name='stats'),
    path('/create_person',views.createPerson,name="create_person"),
]