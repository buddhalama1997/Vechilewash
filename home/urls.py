
from django.urls import path
from . import views

urlpatterns =[
   path('about/',views.about, name= 'about') ,
   path('contact/',views.contact, name= 'contact'),
   path('dashboard/',views.dashboard, name= 'dashboard') ,
   path('signUp/',views.user_signup, name= 'signup'),
   path('login/',views.user_login, name= 'login') ,
   path('logout/',views.user_logout, name= 'logout'),
   path('addpost/',views.add_booking, name= 'addpost'),
   path('updatepost/<int:id>/',views.update_booking, name= 'updatepost'),
   path('delete/<int:id>/',views.delete_booking, name= 'deletepost'),
]