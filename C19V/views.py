from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms

# Create your views here.


def home(request):
    context = {'nbar': 'home'}
    return render(request, 'patient_home.html', context)


def health(request):
    context = {'nbar': 'health'}
    return render(request, 'patient_health.html', context)


def stats(request):
    context = {'nbar': 'stats'}
    return render(request, 'statistics.html', context)


def dashboard(request):
    return render(request, 'vc_home.html')


def login(request):
    return render(request, 'login.html')


def loginVC(request):
    return render(request, 'vaccinationcentre.html')


def report(request):
    return render(request, 'vc_report.html')


def createPerson(request):
    form = forms.PersonForm()

    if request.method == 'POST':
        form = forms.PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    dictionary = {'form': form}
    return render(request, 'createperson.html', dictionary)
