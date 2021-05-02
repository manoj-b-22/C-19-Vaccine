from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views


urlpatterns = [
    path('',views.main,name='main'),                                                            # site's main page
    path('home/<str:pk>/', views.home, name="home"),                                            # vaccination person home page    
    path('healthreport/<str:pk>/', views.health, name="health"),                                # vaccination person status page
    path('statistics/<str:pk>/', views.stats, name='stats'),                                    # statistics of vaccinated person
    path('faq/<str:pk>/',views.faqs,name='faq'),                                                # FAQ's of vaccinated person
    path('nearby/vc/',views.nearby,name='nearbyvc'),                                            # to check nearby vaccination centres 
    path('vc/home/<str:pk>/', views.dashboard, name="dashboard"),                               # vaccinaton centre home page
    path('vc/home/edit/<str:pk>/',views.editprofile,name='edit_profile'),                       # to edit details of vaccination centre
    path('vc/report/<str:pk>/', views.report, name="report"),                                   # vaccination centre report page
    path('vc/statistics/<str:pk>/', views.statsVC, name='statsVC'),                             # statistics of vaccinated person
    path('vc/faq/<str:pk>/',views.faqsvc,name='faqVC'),                                         # FAQ's of vaccination centre
    path('vc/faq/<str:pk>/add/',views.addfaq,name='add_faq'),                                   # to add FAQ
    path('vc/faq/<str:pk>/update/<str:id>/',views.updatefaq,name='update_faq'),                 # to update FAQ
    path('login/', views.LoginPatient, name="login"),                                           # login page for vaccination person
    path('vc/report/<str:pk>/registerperson/',views.register,name='register'),                  # register page for vaccination person
    path('logout/',views.LogoutPatient,name='logout'),                                          # logout for vaccination person
    path('vc/login/', views.LoginVC, name="loginvc"),                                           # login for vaccination centre
    path('vc/logout/',views.LogoutVC,name='logoutvc'),                                          # logout for vaccination centre    
    path('vc/register/', views.registerVC, name='registervc'),                                  # register for vaccination centre 
    path('vc/<str:pk>/callambulance',views.call,name='call_ambulance'),                         # to view critical patients
    path('vc/report/<str:pk>/addperson/<str:user>/', views.createPerson, name="create_person"), # to add vaccination person details
    path('vc/report/<str:pk>/updateperson/<str:id>/',views.updatePerson,name="update_person"),  # to update vaccination person details
    path('vc/report/showpatient/<str:pk>/',views.show,name='show_patient'),                     # to show a particular vaccination person details   
    path('statistics/showcentre/<str:pk>/',views.showvc,name='show_centre'),                    # to show a particular vaccination centre details
    path('vc/register/<str:user>/',views.registerCentre,name='create_centre'),                  # to add details of vaccination centre
   
]
