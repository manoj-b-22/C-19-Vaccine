from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from . import models
from . import forms

# Create your views here.


def home(request):
    context = {'nbar': 'home' , 'block':'Patient'}
    return render(request, 'patient_home.html', context)

def health(request):
    context = {'nbar': 'health' , 'block':'Patient'}
    return render(request, 'patient_health.html', context)

def stats(request):
    context = {'nbar': 'stats' , 'block':'Patient'}
    return render(request, 'statistics.html', context)


def dashboard(request):
    context = {'nbar': 'dashboard' , 'block':'VC'}
    return render(request, 'vc_home.html',context)

def report(request):
    context = {'nbar': 'report' , 'block':'VC'}
    return render(request, 'vc_report.html',context)    

def statsVC(request):
    context = {'nbar': 'statsVC' , 'block':'VC'}
    return render(request, 'stats.html',context)  

def Login(request):
    return render(request, 'patient_login.html')

def LoginVC(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request,'Username or Password is incorrect')    

    return render(request, 'vc_login.html')

def LogoutVC(request):
    logout(request)
    return redirect('loginvc')    

def registerVC(request):
    form = forms.CreateUserForm()

    if request.method=='POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account successfully created for '+user)
            return redirect('loginvc')

    context={ 'form':form }
    return render(request,'vc_register.html',context)

#@login_required(login_url='loginvc')
def createPerson(request):
    form = forms.PersonForm()

    if request.method == 'POST':
        form = forms.PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report')

    dictionary = {'form': form}
    return render(request, 'createperson.html', dictionary)
