from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('HealthReport/', views.health, name="health"),
    path('Statistics/', views.stats, name='stats'),
    path('VaccinationCentre/', views.dashboard, name="dashboard"),
    path('VC/Report/', views.report, name="report"),
    path('Login/', views.login, name="login"),
    path('LoginVC/', views.loginVC, name="loginvc"),
    path('create_person/', views.createPerson, name="create_person"),
]
