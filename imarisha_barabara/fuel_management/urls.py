# fuel_management/urls.py
from django.urls import path
from .views import fuel_log_list, add_fuel_log, generate_pdf

urlpatterns = [
    path('fuel-log-list/', fuel_log_list, name='fuel_log_list'),
    path('add-fuel-log/', add_fuel_log, name='add_fuel_log'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    # Add other URLs as needed
]
