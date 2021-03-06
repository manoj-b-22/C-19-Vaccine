from django.db import models
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms

# Create your views here.


def home(request):
    return render(request,'patient_home.html')

def health(request):
    return render(request,'patient_health.html')

def stats(request):
    return render(request,'statistics.html')

def dashboard(request):
    return render(request,'vc_home.html')

def report(request):
    return render(request,'vc_report.html')    

def createPerson(request):
    form = forms.PersonForm()

    if request.method=='POST':
        form = forms.PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    dictionary = {'form': form}
    return render(request,'createperson.html',dictionary)        
