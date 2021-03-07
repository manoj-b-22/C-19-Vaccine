from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/', views.home, name="home"),
    path('HealthReport/<str:pk>/', views.health, name="health"),
    path('Statistics/<str:pk>/', views.stats, name='stats'),
    path('VaccinationCentre/<str:pk>/', views.dashboard, name="dashboard"),
    path('VC/Report/<str:pk>/', views.report, name="report"),
    path('StatisticsVC/<str:pk>/', views.statsVC, name='statsVC'),
    path('Login/', views.Login, name="login"),
    path('LoginVC/', views.LoginVC, name="loginvc"),
    path('create_person/', views.createPerson, name="create_person"),
    path('RegisterVC/',views.registerVC,name='RegisterVC'),
]
