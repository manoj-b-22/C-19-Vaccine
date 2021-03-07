from django.urls import path
from . import views

urlpatterns = [
    path('home/<str:pk>/', views.home, name="home"),
    path('healthreport/<str:pk>/', views.health, name="health"),
    path('statistics/<str:pk>/', views.stats, name='stats'),
    path('vc/home/<str:pk>/', views.dashboard, name="dashboard"),
    path('vc/report/<str:pk>/', views.report, name="report"),
    path('vc/statistics/<str:pk>/', views.statsVC, name='statsVC'),
    path('login/', views.Login, name="login"),
    path('vc/login/', views.LoginVC, name="loginvc"),
    path('create_person/', views.createPerson, name="create_person"),
    path('vc/register/', views.registerVC, name='registervc'),
]
