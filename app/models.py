from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.conf import settings 

# Create your models here.
class CustomUser(AbstractUser): 
    phone = PhoneNumberField(region="GH") 
    term=models.BooleanField(default=False)
    profile_pic=models.ImageField(upload_to='uploads/profile_pic/', null=True, blank=True) 
 

class RidePost(models.Model):
    # User who posted
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Route details
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    available_seats = models.PositiveIntegerField()
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2)

    # Vehicle info
    car_model = models.CharField(max_length=100)
    car_year = models.PositiveIntegerField(null=True, blank=True)
    car_color = models.CharField(max_length=50, blank=True)
    license_plate = models.CharField(max_length=50)

    # File uploads
    driver_license = models.ImageField(upload_to='uploads/licenses/', null=True, blank=True)
    gh_card_front = models.ImageField(upload_to='uploads/ghcard_front/', null=True, blank=True)
    gh_card_back = models.ImageField(upload_to='uploads/ghcard_back/', null=True, blank=True)
    car_photo = models.ImageField(upload_to='uploads/car_photos/', null=True, blank=True)
                                                                     
    # Preferences
    amenities = models.JSONField(default=list, blank=True)  
    luggage_space = models.CharField(max_length=50, choices=[
        ('small', 'Small bags only'),
        ('medium', 'Medium luggage (1 per passenger)'),
        ('large', 'Large luggage possible'),
    ])
    additional_info = models.TextField(blank=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    ride_status=models.CharField(max_length=20, choices=[
        ('active', 'Active'), 
        ('cancelled', 'Cancelled'),  
    ], default='active') 

    allowed_post=models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.driver}"
    
    class Meta:
        indexes = [
            models.Index(fields=['departure']),
            models.Index(fields=['destination']),
            models.Index(fields=['departure_date']),
            models.Index(fields=['ride_status', 'allowed_post', 'available_seats']),
        ]


class My_booking(models.Model):
    ride = models.ForeignKey(RidePost, on_delete=models.CASCADE, related_name='bookings')
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    # seats_booked = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'), 
        ('cancelled', 'Cancelled'),  
    ], default='active') 
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booked_by.username} for {self.ride.driver.username} {self.status}" 



# class my_rides(models.Model):
#     myride=models.ForeignKey(RidePost,on_delete=models.CASCADE) 
#     passengers=models.ForeignKey(My_booking,on_delete=models.CASCADE) 




