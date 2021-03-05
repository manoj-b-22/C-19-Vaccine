from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.


def home(request):
    return render(request,'login.html')

def centres(request):
    return render(request,'vaccinationcentre.html')    
