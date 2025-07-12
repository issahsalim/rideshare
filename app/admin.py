from django.contrib import admin
from .models import * 
from django.contrib.auth.admin import UserAdmin 
from django.core.mail import send_mass_mail,send_mail
from django.conf import settings

# Register your models here.
class CustomUserAdmin(UserAdmin): 
    list_display=('username','first_name','last_name','phone','term','is_superuser' )  
    search_fields=('username','phone','first_name','last_name') 
    
    fieldsets=(
        (None,{'fields':('username','password')}),
        ('Personal Info',{'fields':('phone','first_name','last_name','email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions','term')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),

    )


    add_fieldsets = (
    (None, {
        'es': ('wide',),
        'fields': ('username', 'email','phone', 'password1', 'password2', 'is_staff','term' 'is_active',),
    }),
)


    ordering=('username',) 

admin.site.register(CustomUser,CustomUserAdmin)


@admin.register(RidePost)
class RidePostAdmin(admin.ModelAdmin):
    search_fields=("driver","destination",)
    list_display = ['driver', 'departure', 'destination', 'departure_date', 'allowed_post']

    def save_model(self, request, obj, form, change):
        previously_allowed = RidePost.objects.get(pk=obj.pk).allowed_post if obj.pk else False
        super().save_model(request, obj, form, change)

        #  Only send email when allowed_post changed from False → True
        if not previously_allowed and obj.allowed_post:
            user_emails = list(CustomUser.objects.exclude(email=obj.driver.email).values_list('email', flat=True))

            subject = "New Ride Approved!"
            message = f"""
            Hello,

            A ride has just been approved by the admin on RideShare Ghana:

            Trip: {obj.departure} → {obj.destination}
            Date: {obj.departure_date}
            Time: {obj.departure_time}
            Price: GHS {obj.price_per_seat} per seat

            Hurry and book now!

            - RideShare Ghana 
            """
            from_email = settings.EMAIL_HOST_USER

            send_mass_mail(
                [(subject, message, from_email, [email]) for email in user_emails],
                fail_silently=False
            )

    # send mail to driver 
            driver_email = obj.driver.email  

            subject = "Your Ride Has Been Approved "
            message = f"""
            Hi {obj.driver.username},

            Your ride from {obj.departure} to {obj.destination} on {obj.departure_date} at {obj.departure_time} has been successfully approved. 🎉

            Passengers can now book your ride on RideShare Ghana.

            Thank you for using RideShare Ghana! 🇬🇭
            """

            from_email = settings.EMAIL_HOST_USER

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[driver_email],
                    fail_silently=False
                )
            except Exception as e:
                print("Error sending mail:", e)



@admin.register(My_booking)
class MyBooksAdmin(admin.ModelAdmin):
     list_display=('booked_by','ride','status',) 
     search_fields=("booked_by","ride",)

# @admin.register(my_rides)
# class MyRidesAdmin(admin.ModelAdmin):
#      list_display=('passengers',) 
#      search_fields=("passengers", )

# admin.site.register(My_booking)