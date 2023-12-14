# fuel_management/models.py
from django.db import models

class FuelLog(models.Model):
    ward = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100)
    number_plate = models.CharField(max_length=20)
    fuel_units = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_litre = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    # Add other fields as needed

    def total_amount_spent(self):
        return self.fuel_units * self.price_per_litre
