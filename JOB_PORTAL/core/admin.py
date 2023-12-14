from django.contrib import admin
from core.models import *


class AdminServices(admin.ModelAdmin):
    list_display = ['name','price']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone','email','password', 'gender']

class AdminAppointment(admin.ModelAdmin):
    list_display = ['your_name','your_phone','your_email','your_service', 'status', 'number_of_people']    

class AdminBookingSlot(admin.ModelAdmin):
    list_display = ['date_time','is_available']    

# Register your models here.
admin.site.register(Service, AdminServices)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Appointment, AdminAppointment)
admin.site.register(BookingSlot, AdminBookingSlot)