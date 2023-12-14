from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
from django.utils import timezone
# from dashboard.models import Staff

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/productImg')


    def __str__(self):
        return self.name


    @staticmethod
    def get_all_services():
        return Service.objects.all()

    @staticmethod
    def get_services_count():
    	return Service.objects.count()


class Customer(models.Model):
	GenderChoice = (
        ("0","Male"),
        ("1","Female"),
        )

	first_name = models.CharField(max_length=20, null=True)
	last_name = models.CharField(max_length=20, null=True)
	address = models.CharField(max_length=500, null=True)
	phone = models.CharField(max_length=10, null=True)
	gender = models.IntegerField(choices=GenderChoice, default=1)
	email = models.CharField(max_length=100, null=True)
	password = models.CharField(max_length=8, null=True)

	def register(self):
		self.save()

	@staticmethod	
	def get_all_customers():
		return Customer.objects.all()

	@staticmethod 
	def get_customers_count():
		return Customer.objects.count()	

	@staticmethod
	def get_customer_by_email(email):
		try:
			return Customer.objects.get(email = email)
		except:
			return False

	def isExists(self):
		if Customer.objects.filter(email = self.email):
			return True
		return False 	

class BookingSlot(models.Model):
    date_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    def check_availability(self):
        # Implement logic to check if the slot is available based on current time, staff, etc.
        now = datetime.now()
        if self.date_time <= now:
            self.is_available = False
        else:
            self.is_available = True
        self.save()

from django.db import models

class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey('dashboard.Staff', on_delete=models.CASCADE, null=True, blank=True)
    your_name = models.CharField(max_length=100)
    your_phone = models.CharField(max_length=10)
    your_email = models.EmailField(max_length=200)
    your_service = models.ForeignKey('Service', on_delete=models.CASCADE, default=1)

    booking_slot = models.ForeignKey(BookingSlot, on_delete=models.CASCADE, null=True, blank=True)

    # New fields
    product = models.ForeignKey('dashboard.Product', on_delete=models.CASCADE, null=True, blank=True)
    number_of_people = models.PositiveIntegerField(default=1)
    
    # Separate fields for date and time
    your_date = models.DateField(default=timezone.now)
    your_time = models.TimeField()

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')


    @staticmethod
    def get_all_appointments():
        return Appointment.objects.all()

    @staticmethod
    def get_appoint_count():
        return Appointment.objects.count()

    @staticmethod
    def get_appointment_by_customer(customer_id):
        return Appointment.objects.filter(customer=customer_id)
    
    # @staticmethod
    # def get_appointment_by_staff(staff_id):
    #     return Appointment.objects.filter(staff=staff_id)
    
    @staticmethod
    def get_pending_appointments_by_staff(staff_id):
        # Your logic to retrieve pending appointments associated with the staff
        return Appointment.objects.filter(staff=staff_id, status='Pending')
    
    @staticmethod
    def get_delivered_appointments_by_staff(staff_id):
        # Your logic to retrieve pending appointments associated with the staff
        return Appointment.objects.filter(staff=staff_id, status='Delivered')

class ChatMessage(models.Model):
    user = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


