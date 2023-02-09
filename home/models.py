from django.db import models

# create a table for blogPost with title and description as field name
class ServiceBook(models.Model):
    serviceType = models.CharField(max_length=100)
    problemInVechile = models.TextField()
    serviceDate = models.DateField()
    serviceTime = models.TimeField()
    bookingStatus = models.CharField(max_length=50, default='requested')
