from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from phonenumber_field.formfields import PhoneNumberField as FormPhoneNumberField
from django.utils import timezone
from .models import *


class SignupForm(UserCreationForm):
    phone = FormPhoneNumberField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':'+233123456789'}))

    password1= forms.CharField(
         widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password','id':'password'})
    )

    password2= forms.CharField(
         widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm Password','id':'c_password'})
    )

    term= forms.BooleanField(
        required=True,
        label="I agree to the Terms and Privacy Policy",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input','id':'agree'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password1', 'password2','term','profile_pic' ]
        
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'first name',}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'last name',}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email',}),
            'username':forms.TextInput(attrs={'class':'form-control  ','placeholder':'username', }),  
            'profile_pic':forms.FileInput(),
        } 



class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'username',
            'id': 'email',  
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'id': 'password',
            'class': 'form-control'
        })
    )


 

class RidePostForm(forms.ModelForm):
    AMENITIES_CHOICES = [
        ('ac', 'Air Conditioning'),
        ('wifi', 'WI-FI'),
        ('usb', 'USB Charging'),
        ('non-smoking', 'No Smoking'),
        ('men', 'Men ONLY'),
        ('women', 'Women ONLY'),
    ]

    amenities = forms.MultipleChoiceField(
        choices=AMENITIES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Amenities"
    )

    class Meta:
        model = RidePost
        fields = [
            'departure', 'destination', 'departure_date', 'departure_time',
            'available_seats', 'price_per_seat',
            'car_model', 'car_year', 'car_color', 'license_plate',
            'driver_license', 'gh_card_front', 'gh_card_back', 'car_photo',
            'amenities', 'luggage_space', 'additional_info'
        ]

        widgets = {
            'departure': forms.TextInput(attrs={
                'placeholder': 'City or specific location',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'destination': forms.TextInput(attrs={
                'placeholder': 'City or specific location',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'departure_date': forms.DateInput(attrs={
                'type': 'date',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'departure_time': forms.TimeInput(attrs={
                'type': 'time',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'available_seats': forms.NumberInput(attrs={
                'placeholder': 'e.g. 4',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'price_per_seat': forms.NumberInput(attrs={
                'placeholder': 'e.g. 50',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'car_model': forms.TextInput(attrs={
                'placeholder': 'e.g. Corolla',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'car_year': forms.NumberInput(attrs={
                'placeholder': 'e.g. 2020',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'car_color': forms.TextInput(attrs={
                'placeholder': 'e.g. Red',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'license_plate': forms.TextInput(attrs={
                'placeholder': 'e.g. GR 1234-20',
                'style': 'padding-left: 30px;',
                'class': 'form-control'
            }),
            'driver_license': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'padding-left: 30px;',
                'id':'licence'
            }),
            'gh_card_front': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'padding-left: 30px;',
                'id':'ghcardf' 
            }), 
            'gh_card_back': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'padding-left: 30px;',
                'id':'ghcardb'
            }),
            'car_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'padding-left: 30px;',
                'id':'carPhoto'
            }), 
            'amenities': forms.CheckboxSelectMultiple(),
            'luggage_space': forms.Select(attrs={
                'class': 'form-control',
                'style': 'padding-left: 30px;'
            }),
            'additional_info': forms.Textarea(attrs={
                'placeholder': 'Any special instructions or meeting point...',
                'rows': 4,
                'class': 'form-control',
                'style': 'padding-left: 30px;'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        departure_time = cleaned_data.get('departure_time')

        if departure_date and departure_time:
            from datetime import datetime
            ride_datetime = datetime.combine(departure_date, departure_time)
            ride_datetime = timezone.make_aware(ride_datetime)

            if ride_datetime < timezone.now():
                raise forms.ValidationError("You cannot select a past date and time for the ride.")

        return cleaned_data


 
#  EDIT PROFILE
class ProfileEditForm(forms.ModelForm):
    phone = FormPhoneNumberField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':'+233123456789'}))

    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'profile_pic']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }