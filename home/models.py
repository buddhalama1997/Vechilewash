from django.db import models
from datetime import datetime,date
from django.contrib.auth.models import User
# create a table for blogPost with title and description as field name
class ServiceBook(models.Model):
    serviceType = models.CharField(max_length=100)
    problemInVechile = models.TextField()
    serviceDate = models.DateField(default= date.today())
    serviceTime = models.TimeField(default= datetime.now().strftime('%H:%M'))
    bookingStatus = models.CharField(max_length=50, default='requested')
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
