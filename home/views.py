# Create your views here.
from .forms import FeedbackForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignUpForm, loginForm,postForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import ServiceBook
from django.core.mail import send_mail
from datetime import datetime,date
#Home
def home(request):
    posts = ServiceBook.objects.all()
    return render(request,'vehicle/home.html',{'posts':posts})

#about
def about(request):
    return render(request,'vehicle/about.html')

#contact
def contact(request):
    return render(request,'vehicle/contact.html')
#billing
def billing(request):
    return render(request,'vehicle/billing.html')


# dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = ServiceBook.objects.all()
        user = request.user

        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'vehicle/dashboard.html',{'posts':posts,'fname':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/vehicle/login/')

#SignUp
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations! You have registered Successfully.')
            user = form.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request,'vehicle/signup.html',{'form':form})

#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = loginForm(request = request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully !!')
                    return HttpResponseRedirect('/vehicle/dashboard/')
        else:
            form = loginForm()
        return render(request,'vehicle/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/vehicle/dashboard/')

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#add new post
def add_booking(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = postForm(request.POST)
            if form.is_valid():
                serviceType = form.cleaned_data['serviceType']
                problemInVechile = form.cleaned_data['problemInVechile']
                serviceDate = form.cleaned_data['serviceDate']
                serviceTime = form.cleaned_data['serviceTime']
                currentdate = date.today()
                if serviceDate >= currentdate:
                    pst = ServiceBook(serviceType=serviceType, problemInVechile = problemInVechile, serviceDate = serviceDate,serviceTime = serviceTime)
                    pst.save()
                    if pst is not None:
                        messages.success(request,'Successfully booked!!')
                        form = postForm()
                else:
                    messages.error(request,'date is not valid!! Please choose the correct date.')
            
                # print(customerid)
                
        else:
            form = postForm()
        return render(request, 'vehicle/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/vehicle/login/')

#update/edit post
def update_booking(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = ServiceBook.objects.get(pk=id)
            form = postForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                if form is not None:
                    messages.success(request,'Booking is Updated Successfully!!')
        else:
            pi = ServiceBook.objects.get(pk=id)
            form = postForm(instance=pi)
        return render(request, 'vehicle/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/vehicle/login/')

#delete post
def delete_booking(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = ServiceBook.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/vehicle/dashboard/')
    else:
        return HttpResponseRedirect('/vehicle/login/')



def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # send email
            subject = 'Feedback from {}'.format(name)
            from_email = email
            recipient_list = ['sanjithasaru123124@gmail.com']
            html_message = '<p>Name: {}</p><p>Email: {}</p><p>Message: {}</p>'.format(name, email, message)
            send_mail(subject, '', from_email, recipient_list, html_message=html_message)
            return render(request, 'vehicle/feedback_thankyou.html')
    else:
        form = FeedbackForm()
    return render(request, 'vehicle/feedback_form.html', {'form': form})
#thankyoupage
def thankyou(request):
    return render(request,'vehicle/feedback_form.html')