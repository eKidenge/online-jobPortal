from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.core.cache import cache
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from dashboard.middlewares.auth import auth_middleware
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from core.models import Service, Customer, Appointment,ChatMessage
from core.views import *
from dashboard import views
from dashboard.models import Product,Staff
from .forms import BookingForm
from django.http import JsonResponse
import json
# from dashboard.forms import AdminForm

# Create your views here.
def index(request):
    try:
        services = Service.get_all_services()
        products = Product.get_all_products()
    except Exception as e:
        # Handle any exceptions here, such as database errors
        services = []  # Set to an empty list or handle the error appropriately
        products = []

    return render(request, 'core/index.html', {'services': services, 'products': products})
def index2(request):
	
	return render(request, 'core/index2.html')

def userHome(request):
	
	return render(request, 'core/userHome.html')

def staffHome(request):
	
	return render(request, 'core/staffHome.html')

def services_and_products(request):
    services = Service.get_all_services()
    products = Product.get_all_products()
    
    return render(request, 'core/servicetable.html', {
        'services': services,
        'products': products,
    })

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')  

def contactForm(request):
    return render(request, 'core/contactForm.html')  

@auth_middleware
def appointments(request):
    customer = request.session.get('customer')
    search_name_query = request.GET.get('search_name', '')
    search_date_query = request.GET.get('search_date', '')

    # Filter appointments based on the search queries
    appointments = Appointment.get_appointment_by_customer(customer).filter(
        your_name__icontains=search_name_query,
        your_date__icontains=search_date_query
    )

    pending_appointments = []
    delivered_appointments = []

    for appointment in appointments:
        if appointment.status != 'Delivered':
            pending_appointments.append(appointment)
        else:
            delivered_appointments.append(appointment)

    return render(request, 'core/appointments.html', {
        'pending_appointments': pending_appointments,
        'delivered_appointments': delivered_appointments,
        'appointments': appointments,
        'search_name_query': search_name_query,  # Pass the search name query to the template
        'search_date_query': search_date_query,  # Pass the search date query to the template
    })
from django.db.models import Q

def pendingAppointments(request):
    staff = request.session.get('staff')
    search_name = request.GET.get('search_name')
    search_date = request.GET.get('search_date')

    appointments = Appointment.get_pending_appointments_by_staff(staff)

    if search_name:
        appointments = appointments.filter(your_name__icontains=search_name)
    
    if search_date:
        appointments = appointments.filter(your_date=search_date)

    return render(request, 'core/pendingAppointments.html', {'appointments': appointments, 'search_name_query': search_name, 'search_date_query': search_date})


def deliveredAppointments(request):
    staff = request.session.get('staff')
    search_name = request.GET.get('search_name')
    search_date = request.GET.get('search_date')

    appointments = Appointment.get_delivered_appointments_by_staff(staff)

    if search_name:
        appointments = appointments.filter(your_name__icontains=search_name)
    
    if search_date:
        appointments = appointments.filter(your_date=search_date)

    return render(request, 'core/deliveredAppointments.html', {'appointments': appointments, 'search_name_query': search_name, 'search_date_query': search_date})


from django.http import JsonResponse
from django.shortcuts import render, redirect

# Add this import at the top of your views.py file
from django.http import Http404

# Your view function
from django.http import JsonResponse

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie




def bookappointment(request):
    services = Service.objects.all()
    products = Product.objects.all()
    staffs = Staff.objects.all()

    form = BookingForm(products=products, staffs=staffs)

    try:
        if request.method == 'POST':
            form = BookingForm(request.POST, products=products, staffs=staffs)

            if form.is_valid():
                customer_id = request.session.get('customer')
                customer = Customer.objects.get(id=customer_id)

                your_service_instance = form.cleaned_data['your_service']
                your_service_id = your_service_instance.id

                product_instance = form.cleaned_data['product']
                product_id = product_instance.id if product_instance else None

                staff_instance = form.cleaned_data['staff']
                staff_id = staff_instance.id if staff_instance else None

                your_name = form.cleaned_data['your_name']
                your_phone = form.cleaned_data['your_phone']
                your_email = form.cleaned_data['your_email']
                your_date = form.cleaned_data['your_date']
                your_time = form.cleaned_data['your_time']
                number_of_people = form.cleaned_data['number_of_people']

                your_service = Service.objects.get(id=your_service_id)
                product = Product.objects.get(id=product_id) if product_id else None
                staff = Staff.objects.get(id=staff_id) if staff_id else None

                appointment = Appointment(
                    customer=customer,
                    your_name=your_name,
                    your_phone=your_phone,
                    your_email=your_email,
                    your_service=your_service,
                    product=product,
                    your_date=your_date,
                    your_time=your_time,
                    staff=staff,
                    number_of_people=number_of_people
                )
                appointment.save()

               # Calculate the total price based on the price of the service and the number of people
                total_price = calculate_total_price(appointment.your_service, appointment.number_of_people)
                # Create the appointment_details dictionary
                appointment_details = {
                    'your_name': appointment.your_name,
                    'your_email': appointment.your_email,
                    'your_service': appointment.your_service,
                    'number_of_people': appointment.number_of_people,
                    'total_price': total_price,
                    'your_date': appointment.your_date,
                    'your_time': appointment.your_time,
                }

                # Create the response_data dictionary
                response_data = {
                    'message': 'Appointment saved successfully',
                    'appointment_details': appointment_details,
                }

                if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    # Check if the request has the AJAX header
                    return JsonResponse(response_data)
                else:
                    # Non-AJAX request, render the template with success message
                    return render(request, 'core/success.html', {'success_message': 'Thank you for choosing our spa! Your appointment is confirmed.', 'appointment_details': appointment_details})

            errors = form.errors.as_json()
            response_data = {'errors': errors}
            return JsonResponse(response_data, status=400)

        # For non-AJAX requests, render the template
        return render(request, 'core/bookappointment.html', {'services': services, 'products': products, 'staffs': staffs, 'form': form})

    except Exception as e:
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=500)
    

def calculate_total_price(service, number_of_people):
    # Add your logic to get the price of the service and calculate the total price
    service_price = service.price  # Adjust this based on your Service model structure
    return service_price * int(number_of_people)

def signup(request):
	if request.method == 'GET':
		return render(request, 'core/signup.html')
	else:
		first_name = request.POST.get('fname')
		last_name = request.POST.get('lname')
		address = request.POST.get('address')
		phone = request.POST.get('phone')
		email = request.POST.get('email')
		password = request.POST.get('password')

		# Validation
		value = {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'phone': phone,
            'email': email
        }

		customer = Customer(first_name = first_name, last_name = last_name, address = address, phone = phone, email = email, password = password)
		
		error_msg = None
		# Saving
		if(not error_msg):
			customer.password = make_password(customer.password)
			customer.register()
			return redirect('index')
		else:
			data = {
				'error': error_msg,
				'values': value 
			}
			return render(request, 'core/login.html', data)
	
def login(request):
    return_url = None

    if request.method == 'GET':
        return_url = request.GET.get('return_url')
        return render(request, 'core/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_msg = None

        if customer:
            if check_password(password, customer.password):
                request.session['customer'] = customer.id
                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return redirect('userHome')
            else:
                error_msg = 'Email or Password Invalid!!'
                messages.error(request, error_msg)
        else:
            error_msg = 'Email or Password Invalid!!'
            messages.error(request, error_msg)

    return render(request, 'core/login.html')

def staffLogin(request):
    return_url = None
    if request.method == 'GET':
        staffLogin.return_url = request.GET.get('return_url')
        return render(request, 'core/staffLogin.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        staff = Staff.get_staff_by_email(email)
        error_msg = None

        # Add a print statement to check the 'staff' object
        print(f'staff: {staff}')

        if staff:
            flag = check_password(password, staff.password)

            # Add a print statement to check the 'flag' value
            print(f'flag: {flag}')

            if flag:
                request.session['staff'] = staff.id
                if staffLogin.return_url:
                    return HttpResponseRedirect(staffLogin.return_url)
                else:
                    staffLogin.return_url = None
                    return redirect('staffHome')
            else:
                error_msg = 'Email or Password Invalid!!'
        else:
            error_msg = 'Email or Password Invalid!!'

        # Add a print statement to check the 'error_msg' value
        print(f'error_msg: {error_msg}')

        return render(request, 'core/staffLogin.html', {'error': error_msg})


def logout(request):
    request.session.clear()
    return redirect('index')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home') 
    return render(request, 'core/admin_login.html')

def deleteAppointment(request, id):
    if request.method == 'POST':
        appointment = Appointment.objects.get(pk=id)
        appointment.delete()
        return redirect('appointments')
	

def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BookingForm()
    return render(request, 'core/booking.html', {'form': form})

def get_products_and_staff(request):
    service_id = request.GET.get("service_id")
    print(f"Service ID received: {service_id}")
    
    # Query your database to retrieve matching products for the selected service.
    products = Product.objects.filter(service_id=service_id)

    # Query your database to retrieve staff members for the selected service.
    staff = Staff.objects.filter(service__id=service_id)  # Filter staff by service ID

    # Create JSON data to send back to the client
    data = {
        "products": [{"id": product.id, "name": product.name} for product in products],
        "staff": [{"id": staff.id, "name": staff.name} for staff in staff],
    }

    # Return the JSON response
    return JsonResponse(data)


def mark_as_delivered(request, id):
    appointment = Appointment.objects.get(pk=id)
    appointment.status = 'Delivered'
    appointment.save()
    return redirect('pendingAppointments') 


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        message = request.POST.get('message')
        if user and message:
            ChatMessage.objects.create(user=user, message=message)
            return JsonResponse({'status': 'Message sent'})
    return JsonResponse({'status': 'Message not sent'}, status=400)

def get_messages(request):
    messages = ChatMessage.objects.all().values('user', 'message', 'timestamp')
    return JsonResponse(list(messages), safe=False)

def consultation(request):
    return render(request, 'core/consult.html')

def chat_interface(request):
    return render(request, 'core/consultation.html')