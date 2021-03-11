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
    path('vc/register/', views.registerVC, name='registervc'),
    path('vc/report/<str:pk>/addperson', views.createPerson, name="create_person"),
    path('healthreport/<str:pk>/addstatus',views.createStatus,name='create_status'),
    path('vc/report/<str:pk>/searchpatient',views.search,name='search_patient'),
    path('vc/report/showpatient/<str:pk>',views.show,name='show_patient'),
    path('/statistics/showcentre/<str:pk>',views.showvc,name='show_centre'),
    path('vc/register/info',views.registerCentre,name='create_register')
]
