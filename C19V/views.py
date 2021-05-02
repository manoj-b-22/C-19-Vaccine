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

# site's main page
def main(request):

    return render(request,'home.html')

# vaccinated person home page
@decorators.patient_required(login_url='login')
def home(request,pk):             # pk is ID of a vaccinated person
    
    person = models.VaccinatedPerson.objects.get(id=pk)
    status = models.Status.objects.filter(person=person).last()  # last status of the person

    green = models.Status.objects.filter(person=person).filter(status='Good').count()    # Count of Good status of that person 
    yellow = models.Status.objects.filter(person=person).filter(status='Ok').count()     # Count of Ok status of that person
    red = models.Status.objects.filter(person=person).filter(status='Bad').count()       # Count of Bad status of that person

    total = models.Status.objects.filter(person=person).count()
    if total==0:             # division by zero is not possible. So, we made total to one.
        total=1
                # We made the percentages from the counts.
    green = int((green/total)*100)
    yellow = int((yellow/total)*100)
    red = int((red/total)*100)
                # nbar shows the navigation bar and block shows the type of user in the below context dictionary  
    context = {'nbar': 'home' , 'block':'Patient','person':person,'status':status,'green':green,'red':red,'yellow':yellow}
    return render(request, 'patient_home.html', context)    

# Status of vaccinated person 
@decorators.patient_required(login_url='login')
def health(request,pk):

    person = models.VaccinatedPerson.objects.get(id=pk)
    last1 = models.Status.objects.filter(person=person).last()     # last status of the person 

    if last1 == None:        # we assume the person status is Good just after the vaccination
        last1 = models.Status.objects.create(status='Good',person=person)    
              # Saving the status form after submitting.  
    if request.method == 'POST': 
        form = forms.StatusForm(request.POST)
        if form.is_valid():
            form.save()
            last1 = models.Status.objects.filter(person=person).last()

    form = forms.StatusForm(initial={'status':last1.status,'person':person})   # initializing the form with previous status
    status = models.Status.objects.filter(person=person)             # filtering all status of that person
    context = {'nbar': 'health' , 'block':'Patient','person':person,'status':status,'last':last1,'form':form}
    return render(request, 'patient_health.html', context)

# Statistics of vaccinated person
@decorators.patient_required(login_url='login')
def stats(request,pk):

    person = models.VaccinatedPerson.objects.get(id=pk)

    people = models.VaccinatedPerson.objects.all()
    myFilter = filters.PersonFilter(request.GET,queryset=people)    # Using custom filter from filters.py using django_filter
    people = myFilter.qs

    centres = models.TestCentre.objects.all() 
    city = myFilter.form.cleaned_data['city']
    state = myFilter.form.cleaned_data['state']

    if city != None and len(city)>0:
        centres = centres.filter(city=city)
    if state != None and len(state)>0:
        centres = centres.filter(state=state)   
              
    # Calculating the contribution of each centre from the total count   
    percent=[]
    for cen in centres:
        k = people.filter(centre=cen.name).count()
        res = int(k/people.count()*100)
        percent.append(res)
    people = people.count()        

    context = {'nbar': 'stats' , 'block':'Patient','person':person,'filter':myFilter,'people':people,'centre':centres,'percent':percent}
    return render(request, 'statistics.html', context)

# FAQ's for vaccination centre
@decorators.patient_required(login_url='login')
def faqs(request,pk):

    person = models.VaccinatedPerson.objects.get(id=pk)
    centre = models.TestCentre.objects.get(name=person.centre)
    faq = models.FAQ.objects.all()

    context={'nbar':'faq','User':'Patient','faqs':faq,'person':person,'centre':centre}
    return render(request,'faq.html',context)    

# To show nearby vaccination centres
def nearby(request):

    centre = models.TestCentre.objects.all()

    myFilter = filters.VCFilter(request.GET,queryset=centre)          # custom filter from filters.py using django_filter
    centre = myFilter.qs
    if len(centre)==0:
        city = ''
    else :    
        city = centre[0].city

    context={'centre':centre,'filter':myFilter,'city':city}
    return render(request,'nearbyvc.html',context)

# home page of vaccination centre
@decorators.VC_required(login_url='loginvc')
def dashboard(request,pk):               # pk is ID of a test centre
    
    person = models.TestCentre.objects.get(id=pk)
            # nbar shows the navigation bar and block shows the type of user in the below context dictionary  
    context = {'nbar': 'dashboard' , 'block':'VC','person':person}
    return render(request, 'vc_home.html',context)

# vaccination centre report
@decorators.VC_required(login_url='loginvc')
def report(request,pk):

    person = models.TestCentre.objects.get(id=pk)
    patients = models.VaccinatedPerson.objects.filter(centre=person.name).order_by('-date_created')[:5]    # details of last 5 patients vaccinated in that centre 

    search = models.VaccinatedPerson.objects.all()
    myFilter = filters.PatientFilter(request.GET,queryset=search)         # custom filter from filters.py using django_filter
    search = myFilter.qs

    vaccinations = models.VaccinatedPerson.objects.filter(centre=person.name).count()
    success = 0              # count of vaccinated persons whose previous status is either Good or Ok
    failure = 0              # count of vaccinated persons whose previous status is Bad

    for i in models.VaccinatedPerson.objects.filter(centre=person.name):
        stat = models.Status.objects.filter(person=i).last()
        if stat != None and stat.status == 'Bad':
            failure+=1
        else:
            success+=1  

    context = {'nbar': 'report' , 'block':'VC','person':person,'patients':patients,'vaccinations':vaccinations,'success':success,
                'failure':failure,'filter': myFilter,'people': search}

    return render(request, 'vc_report.html',context) 

# to update details of vaccinated person
@decorators.VC_required(login_url='loginvc')
def updatePerson(request,pk,id):
                              # id is ID of a vaccinated person
    person = models.VaccinatedPerson.objects.get(id=id)
    form = forms.PersonForm(instance=person)                 # Since this is to update , we are sending the instance of the person which is previously created
        # saving the details of the vaccinated person
    if request.method == 'POST':
        form = forms.PersonForm(request.POST,instance=person)
        if form.is_valid():
            form.save()
            return redirect('report',pk=pk)
     
    dictionary = {'form': form,'update':True}                # the attribute update is to identify, the form is an update form                 
    return render(request, 'registerperson.html', dictionary)

# to show the details of critical patients
@decorators.VC_required(login_url='loginvc')
def call(request,pk):
    centre =  models.TestCentre.objects.get(id=pk)
    patients = models.VaccinatedPerson.objects.filter(centre=centre.name)
    serious = []                                  # to store list of patients whose status is bad and vaccinated in that centre

    for i in patients:
        stat = models.Status.objects.filter(person=i).last()
        if stat != None and stat.status == 'Bad':
            serious.append(i)

    context = {'patients':serious}
    return render(request,'callambulance.html',context)        

# to show the details of vaccinated person 
@decorators.VC_required(login_url='loginvc')
def show(request,pk):

   person = models.VaccinatedPerson.objects.get(id=pk)
   status = models.Status.objects.filter(person=person).last()

   context={'person':person ,'status':status}
   return render(request,'showpatient.html',context) 

# to show the details of the vaccination centre
def showvc(request,pk):

    person = models.TestCentre.objects.get(id=pk)
    count = models.VaccinatedPerson.objects.filter(centre=person.name).count()     # count of vaccinated persons vaccinated in that centre

    context={'person':person,'count':count}
    return render(request,'showcentre.html',context)

# FAQ's page for vaccinated centre 
@decorators.VC_required(login_url='loginvc')
def faqsvc(request,pk):

    person = models.TestCentre.objects.get(id=pk)
    faq = models.FAQ.objects.all()
                # to delete an FAQ
    if request.method == 'POST':
        no = request.POST.get('id')
        faqd = models.FAQ.objects.get(id=no)
        faqd.delete()
        return redirect('faqVC',pk=pk)

    context={'nbar':'faqVC','User':'VC','faqs':faq,'person':person}
    return render(request,'faq.html',context)    

# to add an FAQ
@decorators.VC_required(login_url='loginvc')
def addfaq(request,pk):

    form = forms.FAQForm()

    if request.method=='POST':
        form = forms.FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faqVC',pk=pk)

    context={'form':form, 'state':'add'}            # the attribute state is used to know whether it is an add FAQ or update FAQ
    return render(request,'faqform.html',context)   

# to update an FAQ
@decorators.VC_required(login_url='loginvc')
def updatefaq(request,pk,id):

    faq = models.FAQ.objects.get(id=id)
    form = forms.FAQForm(instance=faq)              # since it is an update , we use instance of previously created FAQ 

    if request.method=='POST':
        form = forms.FAQForm(request.POST,instance=faq)
        if form.is_valid():
            form.save()
            return redirect('faqVC',pk=pk)

    context={'form':form,'state':'update'}
    return render(request,'faqform.html',context)

# statistics of vaccinated person
@decorators.VC_required(login_url='loginvc')
def statsVC(request,pk):

    person = models.TestCentre.objects.get(id=pk)

    people = models.VaccinatedPerson.objects.all()
    myFilter = filters.PersonFilter(request.GET, queryset=people)         # Using custom filter from filters.py using django_filter
    people = myFilter.qs

    # Calculating the contribution of each centre from the total count
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

# to add details of vaccinated person
@decorators.VC_required(login_url='loginvc')
def createPerson(request,pk,user):
    centre = models.TestCentre.objects.get(id=pk)     # user is the ID of User created
    user1 = User.objects.get(id=user)
    person = models.VaccinatedPerson.objects.get(user=user1)
    form = forms.PersonForm(instance=person,initial={'centre':centre.name})   # we initialized the centre because the centre is gonna add the vaccinated person 
               # we used the instance = person because the person is created by the django signals after the User(patient) is created 
    if request.method == 'POST':
        form = forms.PersonForm(request.POST,instance=person)
        if form.is_valid():
            form.save()
            return redirect('report',pk=pk)
     
    dictionary = {'form': form,'update':False}          # the attribute update is to know that it is the first time adding the details
    return render(request, 'registerperson.html', dictionary)

# to add the details of centre
def registerCentre(request,user):
    user1 = User.objects.get(id=user)
    centre = models.TestCentre.objects.get(user=user1)
    form = forms.TestCentreForm(instance=centre)
                # we used the instance = centre because the centre is created by the django signals after the User(centre) is created 
    if request.method == 'POST':
        form = forms.TestCentreForm(request.POST,instance=centre)
        if form.is_valid():
            form.save()
            return redirect('loginvc')    

    dic = {'form':form}
    return render(request,'registercentre.html',dic)

# to edit the details of vaccination centre
@decorators.VC_required(login_url='loginvc')
def editprofile(request,pk):
    centre = models.TestCentre.objects.get(id=pk)
    form = forms.TestCentreForm(instance=centre)
    persons = models.VaccinatedPerson.objects.filter(centre=centre.name)

    if request.method == 'POST':
        form = forms.TestCentreForm(request.POST,instance=centre)
        name = request.POST.get('name')                               
            #  to change the centre name in the VaccinatedPerson model of all the vaccinated persons in that centre
        if name != centre.name :
            for person in persons:
                person.centre = name
                person.save()
        if form.is_valid():
            form.save()
            return redirect('dashboard',pk=pk)

    dic = {'form':form,'update':True}
    return render(request,'registercentre.html',dic)

# login for vaccinated person
def LoginPatient(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)     # we used default django authenticate function
        if user is not None and user.is_staff==False:   # if is_staff is false then it is a patient 
            login(request,user)
            person = models.VaccinatedPerson.objects.get(user=user)
            return HttpResponseRedirect(reverse('home',kwargs={'pk':person.id}))
        else:
            messages.info(request,'Username or Password is incorrect')  # if the credentials are wrong, we are sending the message  

    return render(request, 'patient_login.html')
    
# to register for vaccinated person
@decorators.VC_required(login_url='loginvc')
def register(request,pk):
    form = forms.CreateUserForm()

    if request.method=='POST':
        form = forms.CreateUserForm(request.POST)
        form.is_staff=False            
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('create_person',kwargs={'pk':pk,'user':user.id}))

    context={'form':form }
    return render(request,'patient_register.html',context)

# logout for vaccinated person
def LogoutPatient(request):
    logout(request)
    return redirect('login')

# login for vaccination centre
@csrf_protect
def LoginVC(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)        # we used default django authenticate function
        if user is not None and user.is_staff==True:      # if is_staff is true then it is a vaccination centre
            login(request,user)
            centre = models.TestCentre.objects.get(user=user)
            return HttpResponseRedirect(reverse('dashboard',kwargs={'pk':centre.id}))
        else:
            messages.info(request,'Username or Password is incorrect')      # if the credentials are wrong, we are sending the message   

    return render(request, 'vc_login.html')

# logout for vaccination centre
def LogoutVC(request):
    logout(request)
    return redirect('loginvc')    

# to register for vaccination centre 
@csrf_protect
def registerVC(request):
    form = forms.CreateUserForm()

    if request.method=='POST':
        form = forms.CreateUserForm(request.POST)
        form.is_staff=True
        if form.is_valid():
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account successfully created for '+username)       # if the credentials are correct, we are sending the success message 
            return HttpResponseRedirect(reverse('create_centre',kwargs={'user':user.id}))

    context={'form':form }
    return render(request,'vc_register.html',context)


