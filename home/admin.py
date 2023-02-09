from django.contrib import admin
from .models import ServiceBook
# Register your models here.
@admin.register(ServiceBook)

class postModelAdmin(admin.ModelAdmin):
    list_display = ['serviceType','problemInVechile','serviceDate','serviceTime','bookingStatus']