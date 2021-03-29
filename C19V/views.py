from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

from . import filters
from . import models
from . import forms  
from . import decorators


def main(request):

    return render(request,'home.html')

@decorators.patient_required(login_url='login')
def home(request,pk):
    
    person = models.VaccinatedPerson.objects.get(id=pk)
    status = models.Status.objects.filter(person=person).last()

    green = models.Status.objects.filter(person=person).filter(status='Good').count()
    yellow = models.Status.objects.filter(person=person).filter(status='Ok').count()
    red = models.Status.objects.filter(person=person).filter(status='Bad').count()

    total = models.Status.objects.filter(person=person).count()
    if total==0:
        total=1

    green = int((green/total)*100)
    yellow = int((yellow/total)*100)
    red = int((red/total)*100)

    context = {'nbar': 'home' , 'block':'Patient','person':person,'status':status,'green':green,'red':red,'yellow':yellow}
    return render(request, 'patient_home.html', context)    

@decorators.patient_required(login_url='login')
def health(request,pk):

    person = models.VaccinatedPerson.objects.get(id=pk)
    last1 = models.Status.objects.filter(person=person).last()

    if last1 == None:
        last1 = models.Status.objects.create(status='Good',person=person)

    if request.method == 'POST':
        form = forms.StatusForm(request.POST)
        if form.is_valid():
            form.save()
            last1 = models.Status.objects.filter(person=person).last()

    form = forms.StatusForm(initial={'status':last1.status,'person':person})
    status = models.Status.objects.filter(person=person)
    context = {'nbar': 'health' , 'block':'Patient','person':person,'status':status,'last':last1,'form':form}
    return render(request, 'patient_health.html', context)

@decorators.patient_required(login_url='login')
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
        k = people.filter(centre=cen.name).count()
        res = int(k/people.count()*100)
        percent.append(res)
    people = people.count()        

    context = {'nbar': 'stats' , 'block':'Patient','person':person,'filter':myFilter,'people':people,'centre':centres,'percent':percent}
    return render(request, 'statistics.html', context)

@decorators.patient_required(login_url='login')
def faqs(request,pk):

    person = models.VaccinatedPerson.objects.get(id=pk)
    centre = models.TestCentre.objects.get(name=person.centre)
    faq = models.FAQ.objects.all()

    context={'nbar':'faq','User':'Patient','faqs':faq,'person':person,'centre':centre}
    return render(request,'faq.html',context)    

def nearby(request):

    centre = models.TestCentre.objects.all()

    myFilter = filters.VCFilter(request.GET,queryset=centre)
    centre = myFilter.qs

    context={'centre':centre,'filter':myFilter}
    return render(request,'nearbyvc.html',context)

@decorators.VC_required(login_url='loginvc')
def dashboard(request,pk):
    
    person = models.TestCentre.objects.get(id=pk)

    context = {'nbar': 'dashboard' , 'block':'VC','person':person}
    return render(request, 'vc_home.html',context)

@decorators.VC_required(login_url='loginvc')
def report(request,pk):

    person = models.TestCentre.objects.get(id=pk)
    patients = models.VaccinatedPerson.objects.filter(centre=person.name).order_by('-date_created')[:5]

    search = models.VaccinatedPerson.objects.all()
    myFilter = filters.PatientFilter(request.GET,queryset=search)
    search = myFilter.qs

    vaccinations = models.VaccinatedPerson.objects.filter(centre=person.name).count()
    success = 0 
    failure = 0

    for i in models.VaccinatedPerson.objects.filter(centre=person.name):
        stat = models.Status.objects.filter(person=i).last()
        if stat != None and stat.status == 'Bad':
            failure+=1
        else:
            success+=1  

    context = {'nbar': 'report' , 'block':'VC','person':person,'patients':patients,'vaccinations':vaccinations,'success':success,
                'failure':failure,'filter': myFilter,'people': search}

    return render(request, 'vc_report.html',context) 

@decorators.VC_required(login_url='loginvc')
def updatePerson(request,pk,id):

    person = models.VaccinatedPerson.objects.get(id=id)
    form = forms.PersonForm(instance=person) 

    if request.method == 'POST':
        form = forms.PersonForm(request.POST,instance=person)
        if form.is_valid():
            form.save()
            return redirect('report',pk=pk)
     
    dictionary = {'form': form,'update':True}
    return render(request, 'registerperson.html', dictionary)


@decorators.VC_required(login_url='loginvc')
def call(request,pk):
    centre =  models.TestCentre.objects.get(id=pk)
    patients = models.VaccinatedPerson.objects.filter(centre=centre.name)
    serious = []

    for i in patients:
        stat = models.Status.objects.filter(person=i).last()
        if stat != None and stat.status == 'Bad':
            serious.append(i)

    context = {'patients':serious}
    return render(request,'callambulance.html',context)        

@decorators.VC_required(login_url='loginvc')
def show(request,pk):

   person = models.VaccinatedPerson.objects.get(id=pk)
   status = models.Status.objects.filter(person=person).last()

   context={'person':person ,'status':status}
   return render(request,'showpatient.html',context) 

def showvc(request,pk):

    person = models.TestCentre.objects.get(id=pk)
    count = models.VaccinatedPerson.objects.filter(centre=person.name).count()

    context={'person':person,'count':count}
    return render(request,'showcentre.html',context)

@decorators.VC_required(login_url='loginvc')
def faqsvc(request,pk):

    person = models.TestCentre.objects.get(id=pk)
    faq = models.FAQ.objects.all()

    if request.method == 'POST':
        no = request.POST.get('id')
        faqd = models.FAQ.objects.get(id=no)
        faqd.delete()
        return redirect('faqVC',pk=pk)

    context={'nbar':'faqVC','User':'VC','faqs':faq,'person':person}
    return render(request,'faq.html',context)    

@decorators.VC_required(login_url='loginvc')
def addfaq(request,pk):

    form = forms.FAQForm()

    if request.method=='POST':
        form = forms.FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faqVC',pk=pk)

    context={'form':form, 'state':'add'}
    return render(request,'faqform.html',context)

@decorators.VC_required(login_url='loginvc')
def updatefaq(request,pk,id):

    faq = models.FAQ.objects.get(id=id)
    form = forms.FAQForm(instance=faq)

    if request.method=='POST':
        form = forms.FAQForm(request.POST,instance=faq)
        if form.is_valid():
            form.save()
            return redirect('faqVC',pk=pk)

    context={'form':form,'state':'update'}
    return render(request,'faqform.html',context)

@decorators.VC_required(login_url='loginvc')
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
        k = people.filter(centre=cen.name).count()
        res = int(k/people.count()*100)
        percent.append(res)
    people = people.count()

    context = {'nbar': 'statsVC', 'block': 'VC', 'person': person,'filter': myFilter, 'people': people, 'centre': centres, 'percent': percent}
    return render(request, 'statistics.html',context)

@decorators.VC_required(login_url='loginvc')
def createPerson(request,pk,user):
    centre = models.TestCentre.objects.get(id=pk)
    user1 = User.objects.get(id=user)
    person = models.VaccinatedPerson.objects.get(user=user1)
    form = forms.PersonForm(instance=person,initial={'centre':centre.name}) 

    if request.method == 'POST':
        form = forms.PersonForm(request.POST,instance=person)
        if form.is_valid():
            form.save()
            return redirect('report',pk=pk)
     
    dictionary = {'form': form,'update':False}
    return render(request, 'registerperson.html', dictionary)

def registerCentre(request,user):
    user1 = User.objects.get(id=user)
    centre = models.TestCentre.objects.get(user=user1)
    form = forms.TestCentreForm(instance=centre)

    if request.method == 'POST':
        form = forms.TestCentreForm(request.POST,instance=centre)
        if form.is_valid():
            form.save()
            return redirect('loginvc')

    dic = {'form':form}
    return render(request,'registercentre.html',dic)

@decorators.VC_required(login_url='loginvc')
def editprofile(request,pk):
    centre = models.TestCentre.objects.get(id=pk)
    form = forms.TestCentreForm(instance=centre)
    persons = models.VaccinatedPerson.objects.filter(centre=centre.name)

    if request.method == 'POST':
        form = forms.TestCentreForm(request.POST,instance=centre)
        name = request.POST.get('name')
        if name != centre.name :
            for person in persons:
                person.centre = name
                person.save()
        if form.is_valid():
            form.save()
            return redirect('dashboard',pk=pk)

    dic = {'form':form,'update':True}
    return render(request,'registercentre.html',dic)

def LoginPatient(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_staff==False:
            login(request,user)
            person = models.VaccinatedPerson.objects.get(user=user)
            return HttpResponseRedirect(reverse('home',kwargs={'pk':person.id}))
        else:
            messages.info(request,'Username or Password is incorrect')    

    return render(request, 'patient_login.html')
    

@decorators.VC_required(login_url='loginvc')
def register(request,pk):
    form = forms.CreateUserForm()

    if request.method=='POST':
        form = forms.CreateUserForm(request.POST)
        form.is_staff=False
        if form.is_valid():
            user = form.save()
            person = models.VaccinatedPerson.objects.create(user=user)
            person.save()
            return HttpResponseRedirect(reverse('create_person',kwargs={'pk':pk,'user':user.id}))

    context={'form':form }
    return render(request,'patient_register.html',context)


def LogoutPatient(request):
    logout(request)
    return redirect('login')

@csrf_protect
def LoginVC(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_staff==True:
            login(request,user)
            centre = models.TestCentre.objects.get(user=user)
            return HttpResponseRedirect(reverse('dashboard',kwargs={'pk':centre.id}))
        else:
            messages.info(request,'Username or Password is incorrect')    

    return render(request, 'vc_login.html')

def LogoutVC(request):
    logout(request)
    return redirect('loginvc')    

@csrf_protect
def registerVC(request):
    form = forms.CreateUserForm()

    if request.method=='POST':
        form = forms.CreateUserForm(request.POST)
        form.is_staff=True
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff=True
            user.save()
            centre = models.TestCentre.objects.create(user=user)
            centre.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account successfully created for '+username)
            return HttpResponseRedirect(reverse('create_centre',kwargs={'user':user.id}))

    context={'form':form }
    return render(request,'vc_register.html',context)


