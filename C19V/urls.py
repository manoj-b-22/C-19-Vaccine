from django.urls import path
from . import views

urlpatterns = [
    path('home/<str:pk>/', views.home, name="home"),
    path('healthreport/<str:pk>/', views.health, name="health"),
    path('statistics/<str:pk>/', views.stats, name='stats'),
    path('faq/<str:pk>/',views.faqs,name='faq'),
    path('vc/home/<str:pk>/', views.dashboard, name="dashboard"),
    path('vc/report/<str:pk>/', views.report, name="report"),
    path('vc/statistics/<str:pk>/', views.statsVC, name='statsVC'),
    path('vc/faq/<str:pk>/',views.faqsvc,name='faqVC'),
    path('vc/faq/<str:pk>/add/',views.addfaq,name='add_faq'),
    path('vc/faq/<str:pk>/update/<str:id>/',views.updatefaq,name='update_faq'),
    path('login/', views.LoginPatient, name="login"),
    path('vc/report/<str:pk>/registerperson/',views.register,name='register'),
    path('logout/',views.LogoutPatient,name='logout'),
    path('vc/login/', views.LoginVC, name="loginvc"),
    path('vc/logout/',views.LogoutVC,name='logoutvc'),
    path('vc/register/', views.registerVC, name='registervc'),
    path('vc/<str:pk>/callambulance',views.call,name='call_ambulance'),
    path('vc/report/<str:pk>/addperson/<str:user>/', views.createPerson, name="create_person"),
    path('vc/report/<str:pk>/updateperson/<str:id>/',views.updatePerson,name="update_person"),
    path('vc/report/showpatient/<str:pk>/',views.show,name='show_patient'),
    path('statistics/showcentre/<str:pk>/',views.showvc,name='show_centre'),
    path('vc/register/<str:user>/',views.registerCentre,name='create_centre')
]
