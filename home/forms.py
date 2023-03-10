
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField

from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _

from home.models import ServiceBook


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels ={'first_name': 'First Name', 'last_name':'Last Name'}
        widgets = { 'username': forms.TextInput(attrs={'class':'form-control'}),
                    'first_name': forms.TextInput(attrs={'class':'form-control'}),
                    'last_name': forms.TextInput(attrs={'class':'form-control'}),
                    'email': forms.EmailInput(attrs={'class':'form-control'}),
        }


class loginForm(AuthenticationForm):
    username = UsernameField(widget= forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class postForm(forms.ModelForm):
    class Meta:
        model = ServiceBook
        fields = ['serviceType','problemInVechile','serviceDate','serviceTime']
        widgets = {
                    'serviceType': forms.TextInput(attrs={'class':'form-control'}),
                    'problemInVechile': forms.Textarea(attrs={'class':'form-control'}),
                    'serviceDate': forms.DateInput(attrs={'class':'form-control'}),
                    'serviceTime': forms.TimeInput(attrs={'class':'form-control'})
                }
    
class FeedbackForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Your email', max_length=100)
    message = forms.CharField(label='Your message', widget=forms.Textarea)
