# Create your views here.
import io
from .forms import FeedbackForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import render
from .forms import SignUpForm, loginForm,postForm, ContactForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import ServiceBook
from django.core.mail import send_mail
from datetime import datetime,date

from reportlab.pdfgen import canvas

from django.template.loader import get_template

#Home
def home(request):
    posts = ServiceBook.objects.all()
    return render(request,'vehicle/home.html',{'posts':posts})

#about
def about(request):
    return render(request,'vehicle/about.html')


#billing
def billing(request):
    return render(request,'vehicle/billing.html')

def khalti(request):
    total = request.POST.get('total')
    return render(request,'vehicle/khalti.html',{'total':total})
def khalti_verification(request):
    data ={}
    return JsonResponse(data)

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
                pst = ServiceBook(serviceType=serviceType, problemInVechile = problemInVechile, serviceDate = serviceDate,serviceTime = serviceTime)
                currentdate = date.today()
                if serviceDate < currentdate:
                    messages.error(request,'date is not valid!! Please choose the correct date.')
                    
                else:
                    pst = ServiceBook(serviceType=serviceType, problemInVechile = problemInVechile, serviceDate = serviceDate,serviceTime = serviceTime)
                    pst.save()
                    if pst is not None:
                        messages.success(request,'Successfully booked!!')
                        form = postForm()
                # print(customerid)
        else:
            form = postForm()
        return render(request, 'vehicle/addpost.html',{'form':form})

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
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact_number = form.cleaned_data['contact_number']
            message = form.cleaned_data['message']
            # send email
            subject = 'Contact from {}'.format(name)
            from_email = email
            recipient_list = ['sanjithasaru123124@gmail.com']
            html_message = '<p>Name: {}</p><p>Number: {}</p><p>Email: {}</p><p>Message: {}</p>'.format(name,contact_number, email, message)
            send_mail(subject, '', from_email, recipient_list, html_message=html_message)
            return render(request, 'vehicle/contactthank.html')
    else:
        form = ContactForm()
    return render(request, 'vehicle/contact.html', {'form': form})



def generate_pdf(request):
    if request.method == 'POST':
        if 'bill' in request.POST:
            # Handle Button 1 click
            # Redirect to URL for Button 1
            # Process the form submission and retrieve the form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            total = request.POST.get('total')

            
            buffer = io.BytesIO()

            # Create the PDF object, using the buffer as its "file."
            p = canvas.Canvas(buffer)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.drawString(100, 750, "Pathari Car Wash and Repairing Center")
            p.drawString(100, 700, "Bill Amount")
            p.drawString(100, 650, "Name    :")
            p.drawString(200, 650, name)
            
            p.drawString(100, 600, "Email   :")
            p.drawString(200, 600, email)
            p.drawString(100, 550, "Address :")
            p.drawString(200, 550, address)
            p.drawString(100, 500, "Total    :")
            p.drawString(200, 500, total)
            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            # File response with PDF content.
            pdf = buffer.getvalue()
            buffer.close()
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="hello.pdf"'
            return response

        elif 'online' in request.POST:
            # Handle Button 2 click
            # Redirect to URL for Button 2
            total = request.POST.get('total')
            return render(request,'vehicle/khalti.html',{'total':total})
    else:
        # Render the template for GET request
        return render(request,'vehicle/billing.html') 
    
