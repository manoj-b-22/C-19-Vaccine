from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
<<<<<<< HEAD
    return render(request, 'login.html')


def centres(request):
    return render(request, 'vaccinationcentre.html')
=======
    return render(request,'home.html')

def centre(request):
    return render(request,'vaccinationcentre.html')    
>>>>>>> dbf396d85f150b293b06583fbe6cc04a85cf8aeb
