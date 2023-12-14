from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'), 
   path('signup/', views.signup, name='signup'), 
   path('userHome/', views.userHome, name='userHome'),
   path('staffHome/', views.staffHome, name='staffHome'),
   path('login/', views.login, name='login'),
   path('staffLogin/', views.staffLogin, name='staffLogin'),
   path('user_logout/', views.logout, name='user_logout'),
   path('services/', views.services_and_products, name='services'), 
   path('contact/', views.contact, name='contact'),
   path('contactForm/', views.contactForm, name='contactForm'),
   path('about/', views.about, name='about'),
   path('bookappointment/', views.bookappointment, name='bookappointment'),
   path('booking/', views.booking_view, name='booking'),
   path('deleteAppointment/<int:id>/', views.deleteAppointment, name='deleteAppointment'),
   path('mark_as_delivered/<int:id>/', views.mark_as_delivered, name='mark_as_delivered'),
   path('appointments/', views.appointments, name='appointments'),
   path('pendingAppointments/', views.pendingAppointments, name='pendingAppointments'),
   path('deliveredAppointments/', views.deliveredAppointments, name='deliveredAppointments'),
   path('admin_login/', views.admin_login, name='admin_login'),
   path('index2/', views.index2, name='index2'),
   path('get-products-and-staff/', views.get_products_and_staff, name='get_products_and_staff'),
   path('send_message/', views.send_message, name='send_message'),
   path('get_messages/', views.get_messages, name='get_messages'),
   path('consultation/', views.consultation, name='consultation'),
   path('chat_interface/', views.chat_interface, name='chat_interface'),
   



]


