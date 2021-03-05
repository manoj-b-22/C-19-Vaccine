from django.db import models
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms

# Create your views here.


def home(request):
    return render(request,'login.html')

def centres(request):
    return render(request,'vaccinationcentre.html')    

def createPerson(request):
    form = forms.PersonForm()

    if request.method=='POST':
        form = forms.PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    dictionary = {'form': form}
    return render(request,'',dictionary)        
