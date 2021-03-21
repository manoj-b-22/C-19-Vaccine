from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from . import filters
from . import models
from . import forms

# Create your views here.


def home(request,pk):
    
    person = models.VaccinatedPerson.objects.get(id=pk)
    status = models.Status.objects.filter(person=person).last()

    green = models.Status.objects.filter(person=person).filter(status='Good').count()
    yellow = models.Status.objects.filter(person=person).filter(status='Ok').count()
    red = models.Status.objects.filter(person=person).filter(status='Bad').count()

    total = models.Status.objects.filter(person=person).count()

    green = int((green/total)*100)
    yellow = int((yellow/total)*100)
    red = int((red/total)*100)

    context = {'nbar': 'home' , 'block':'Patient','person':person,'status':status,'green':green,'red':red,'yellow':yellow}
    return render(request, 'patient_home.html', context)

def health(request,pk):

    person = models.VaccinatedPerson.objects.get(id=pk)
    last1 = models.Status.objects.filter(person=person).last()

    if request.method == 'POST':
        form = forms.StatusForm(request.POST)
        if form.is_valid():
            form.save()
            last1 = models.Status.objects.filter(person=person).last()

    form = forms.StatusForm(initial={'status':last1.status,'person':person})
    status = models.Status.objects.filter(person=person)
    context = {'nbar': 'health' , 'block':'Patient','person':person,'status':status,'last':last1,'form':form}
    return render(request, 'patient_health.html', context)

def stats(request,pk):

    person = models.VaccinatedPerson.objects.get(id=pk)

    people = models.VaccinatedPerson.objects.all()
    myFilter = filters.PersonFilter(request.GET,queryset=people)
    people = myFilter.qs

    centres = models.TestCentre.objects.all() 
    city = myFilter.form.cleaned_data['city']
    state = myFilter.form.cleaned_data['state']

    if city != None and len(city)>0:
        centres = centres.filter(city=city)
    if state != None and len(state)>0:
        centres = centres.filter(state=state)   

    percent=[]
    for cen in centres:
        k = people.filter(centre=cen).count()
        res = int( k/people.count()*100)
        percent.append(res)
    people = people.count()        

    context = {'nbar': 'stats' , 'block':'Patient','person':person,'filter':myFilter,'people':people,'centre':centres,'percent':percent}
    return render(request, 'statistics.html', context)


def dashboard(request,pk):
    
    person = models.TestCentre.objects.get(id=pk)

    context = {'nbar': 'dashboard' , 'block':'VC','person':person}
    return render(request, 'vc_home.html',context)

def report(request,pk):

    person = models.TestCentre.objects.get(id=pk)
    patients = models.VaccinatedPerson.objects.filter(centre=person).order_by('-date_created')[:5]

    search = models.VaccinatedPerson.objects.all()
    myFilter = filters.PatientFilter(request.GET,queryset=search)
    search = myFilter.qs

    vaccinations = models.VaccinatedPerson.objects.filter(centre=person).count()
    success = 0 
    failure = 0

    for i in models.VaccinatedPerson.objects.filter(centre=person):
        stat = models.Status.objects.filter(person=i).last()
        if stat != None and stat.status == 'Bad':
            failure+=1
        else:
            success+=1  

    context = {'nbar': 'report' , 'block':'VC','person':person,'patients':patients,'vaccinations':vaccinations,'success':success,
                'failure':failure,'filter': myFilter,'people': search}

    return render(request, 'vc_report.html',context) 

def call(request,pk):
    centre =  models.TestCentre.objects.get(id=pk)
    patients = models.VaccinatedPerson.objects.filter(centre=centre)
    serious = []

    for i in patients:
        stat = models.Status.objects.filter(person=i).last()
        if stat != None and stat.status == 'Bad':
            serious.append(i)

    context = {'patients':serious}
    return render(request,'callambulance.html',context)        

def show(request,pk):

   person = models.VaccinatedPerson.objects.get(id=pk)
   status = models.Status.objects.filter(person=person).last()

   context={'person':person ,'status':status}
   return render(request,'showpatient.html',context) 

def showvc(request,pk):

    person = models.TestCentre.objects.get(id=pk)
    count = models.VaccinatedPerson.objects.filter(centre=person).count()

    context={'person':person,'count':count}
    return render(request,'showcentre.html',context)

def statsVC(request,pk):

    person = models.TestCentre.objects.get(id=pk)

    people = models.VaccinatedPerson.objects.all()
    myFilter = filters.PersonFilter(request.GET, queryset=people)
    people = myFilter.qs

    percent = []
    centres = models.TestCentre.objects.all()
    city = myFilter.form.cleaned_data['city']
    state = myFilter.form.cleaned_data['state']
    if city !=None and len(city)>0:
        centres = centres.filter(city=city)
    if state !=None and len(state)>0:
        centres = centres.filter(state=state)

    for cen in centres:
        k = people.filter(centre=cen).count()
        res = int(k/people.count()*100)
        percent.append(res)
    people = people.count()

    context = {'nbar': 'statsVC', 'block': 'VC', 'person': person,'filter': myFilter, 'people': people, 'centre': centres, 'percent': percent}
    return render(request, 'statistics.html',context)

def Login(request):
    return render(request, 'patient_login.html')

def createPerson(request,pk):

    person = models.TestCentre.objects.get(id=pk)

    if request.method == 'POST':
        form = forms.PersonForm(request.POST)   
        if form.is_valid():
            form.save()
            return redirect('report',pk=pk)

    form = forms.PersonForm(initial={'centre':person})      
    dictionary = {'form': form,}
    return render(request, 'registerperson.html', dictionary)

def registerCentre(request,user):

    if request.method == 'POST':
        form = forms.TestCentreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginvc')

    form = forms.TestCentreForm(initial={'user':user})
    dic = {'form':form}
    return render(request,'registercentre.html',dic)    

def LoginPatient(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')    

    return render(request, 'patient_login.html')

def LogoutPatient(request):
    logout(request)
    return redirect('login')

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

    if request.method=='POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account successfully created for '+username)
            return redirect('create_register',user=user)

    form = forms.CreateUserForm()
    context={ 'form':form }
    return render(request,'vc_register.html',context)

#@login_required(login_url='loginvc')
