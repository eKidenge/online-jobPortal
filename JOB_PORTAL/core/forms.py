# forms.py
from django import forms
from .models import Service,Appointment,BookingSlot
from dashboard.models import Staff,Product

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'service']



class BookingForm(forms.ModelForm):

    TIME_CHOICES = [
        ('09:00', '09:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('02:00', '02:00 PM'),
        ('04:00', '04:00 AM'),
        # Add more time options as needed
    ]
    Reserved_Slots = [
        ('6', '6'),
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
        # Add more time options as needed
    ]
    class Meta:
        model = Appointment
        fields = ['your_name', 'your_phone', 'your_email', 'number_of_people', 'your_date', 'your_time', 'your_service', 'product','staff']
        
    def __init__(self, *args, **kwargs):
        products = kwargs.pop('products', None)
        staffs = kwargs.pop('staffs', None)
        
        super(BookingForm, self).__init__(*args, **kwargs)

        if products is not None:
            self.fields['product'].choices = [(product.id, product.name) for product in products]
        
        if staffs is not None:
            self.fields['staff'].choices = [(staff.id, staff.name) for staff in staffs]

    your_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Enter Full Name'
    )
    your_phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Enter Mobile Number'
    )
    your_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Enter Email Address'
    )
    number_of_people = forms.ChoiceField(
        choices=Reserved_Slots,
        widget=forms.Select(attrs={'class': 'form-select form-control', 'id': 'number_of_people'}),
        label='Reserved Slots'
    )
    your_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'date-picker'}),
        label='Select Date'
    )
    your_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-control', 'id': 'your_time'}),
        label='Appointment Time'
    )

    your_service = forms.ModelChoiceField(
        queryset=Service.objects.all(),  # Queryset to populate service choices
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'service-select'}),
        label='Choose Service...'
    )
    product = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'products-select'}),
        label='Products',
        required=True,  # Make it optional
        choices=[('0', 'Choose Products')]  # Updated default choice
    )

    staff = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'staff-select'}),
        label='Staff',
        required=True,  # Make it optional
        choices=[('0', 'Choose Staff')]  # Updated default choice
    )

    def clean(self):
        cleaned_data = super().clean()
        staff_id = cleaned_data.get('staff')
        product_id = cleaned_data.get('product')

        if staff_id:
            if staff_id == '0':
                cleaned_data['staff'] = None  # No staff selected
            else:
                try:
                    staff = Staff.objects.get(id=int(staff_id))
                    cleaned_data['staff'] = staff
                except Staff.DoesNotExist:
                    self.add_error('staff', 'Invalid staff selection')

        if product_id:
            if product_id == '0':
                cleaned_data['product'] = None  # No product selected
            else:
                try:
                    product = Product.objects.get(id=int(product_id))
                    cleaned_data['product'] = product
                except Product.DoesNotExist:
                    self.add_error('product', 'Invalid product selection')

        return cleaned_data