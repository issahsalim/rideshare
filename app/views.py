from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages 
from  .forms import* 
from   .models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,send_mass_mail
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView 
from django.urls import reverse_lazy 
from datetime import datetime

# Create your views here.
User= get_user_model() 

class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = "email_reset_password.html"
    success_url = reverse_lazy('password_reset_done')  

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        
        
        if User.objects.filter(email=email).exists():
          
            return super().form_valid(form)
        else:
           
            messages.error(self.request, "Email does not match any account")
            return self.form_invalid(form)
   
   

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')   
            else:
                messages.error(request,'Invalid username or password') 
                return redirect('login')

    return render(request, 'login.html', {'form': form})


@login_required
def offer_ride(request):
    if request.method == 'POST':
        form = RidePostForm(request.POST, request.FILES)
        if form.is_valid(): 
            ride = form.save(commit=False)
            # departure_date = request.POST.get('departure_date')
            # departure_time = request.POST.get('departure_time')
            # if departure_date and departure_time:
            #     from datetime import datetime
            #     ride_dt = datetime.strptime(f"{departure_date} {departure_time}", "%d-%m-%Y %H:%M")
            #     from django.utils.timezone import make_aware
            #     ride_dt = make_aware(ride_dt)
            #     if ride_dt<timezone.now():
            #          messages.error(request, "The date and time cannot be in the past.")
            #          return redirect('offer_ride')

            ride.driver = request.user 
            ride.save() 
          
            messages.info(request,' please wait about 5min for a review of you document')
            return redirect('offer_ride')
    else: 
        form = RidePostForm() 
    return render(request, 'offer-ride.html', {'form': form,})


@login_required
def find_ride(request):
    rides = RidePost.objects.filter(ride_status="active")
    
    # Get search filters
    departure = request.GET.get("from")
    destination = request.GET.get("to")
    date = request.GET.get("date")

    # Apply filters if fields are filled
    if departure: 
        rides = rides.filter(departure__icontains=departure)
        if not rides:
            return render(request,'NotFound.html',{'error_notfound':departure})
        return render(request,'find-ride.html',{'searchFound': rides })
    if destination:
        rides = rides.filter(destination__icontains=destination)
        if not rides:
            return render(request,'NotFound.html',{'search_notfound':destination})
        return render(request,'find-ride.html',{'searchFound': rides})
    if date:  
        try:    
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            rides = rides.filter(departure_date=date_obj)
            if not rides:
                return render(request,'NotFound.html',{'search_notfound':destination})
            return render(request,'find-ride.html',{'searchFound': rides})
        except: 
            pass
    if departure and destination and date:
        rides = rides.filter(Q(destination__icontains=destination,departure=destination))
        if not rides:
             return render(request,'NotFound.html',{'search_notfound':destination})
        return render(request,'find-ride.html',{'searchFound': rides})
        
    aviableRide = RidePost.objects.filter(
    allowed_post=True,
    available_seats__gt=0,
    departure_date__gte=timezone.now().date()
)   
    return render(request, "find-ride.html", {'allrides':aviableRide})


# booking a ride ()
def bookBtn(request, id):
    ride = get_object_or_404(RidePost, id=id)
    
    # Check available seats
    if ride.available_seats <= 0:
        messages.error(request, 'No available seats for this ride')
        return redirect('find_ride')
    
    # Check if user already booked this ride
    existing_booking = My_booking.objects.filter(ride=ride, booked_by=request.user).exists()
    if existing_booking:
        messages.warning(request, 'You have already booked this ride')
        return redirect('find_ride')
    
    if ride.ride_status=="cancelled":
        messages.warning(request,"U can't booked this ride because it called by the driver")
        return redirect('find_ride') 


    try:
        # Create the booking first
        booking = My_booking.objects.create(ride=ride, booked_by=request.user)
        
        # Update available seats
        ride.available_seats -= 1
        ride.save()
        
        # Send email notification
        subject = "New Ride Booking Notification"
        message = f"""Hi {ride.driver.username},{request.user.username} has booked your ride from {ride.departure} to {ride.destination} on {ride.departure_date}.        
        Thank you for using our app! 😊"""
        
        from_email = f"RideShare <{settings.EMAIL_HOST_USER}>"
        to_email = [ride.driver.email]
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=to_email,
            fail_silently=False
        )
        
        messages.success(request, 'Successfully booked the ride!')
        return redirect('find_ride')
        
    except Exception as e:
        # If anything fails, delete the booking and revert seats
        if 'booking' in locals():
            booking.delete()
            ride.available_seats += 1
            ride.save()
            
        messages.error(request, f'Failed to complete booking: {str(e)}')
        return redirect('find_ride')


# viewing all user bookings 
@login_required
def my_bookings(request):
    mybooks=My_booking.objects.select_related('ride','booked_by').filter(booked_by=request.user)
    return render(request,'my_bookings.html',{'myboks':mybooks}) 


# cancel btn in my booking page
def cancelBokBtn(request,id):
    cancelbok=get_object_or_404(My_booking,id=id,booked_by=request.user) 
    # if cancelbok.status=="active": 
    cancelbok.status="cancelled" 
    cancelbok.ride.available_seats+=1 
    cancelbok.ride.save()  
    cancelbok.save()   
    try:   
        subject="Booking Cancelled",
        message=f"""Hi {cancelbok.ride.driver.username}, {request.user} has cancel you ride \n\n THANK YOU FOR USING YOUR APP😘"""
        from_mail=f"RideShare <{settings.EMAIL_HOST_USER}>"
        to_mail=[cancelbok.ride.driver.email]   
        send_mail( 
            subject=subject, message=message, from_email=from_mail,recipient_list=to_mail 
        ) 
        
    except Exception as e:      
            messages.warning(request,f"error occur {e}") 
            return redirect('my_booking') 
    messages.success(request,'Ride Successfully cancelled')
    return redirect('my_booking') 


def activateBokBtn(request,id):
    cancelbok = get_object_or_404(My_booking, id=id, booked_by=request.user)
    ride = cancelbok.ride

    # Step 2: Count how many active bookings this ride already has
    active_bookings = My_booking.objects.filter(ride=ride, status="active").count()

    # Step 3: Check if seats are full
    if active_bookings >= ride.available_seats:
        messages.info(request, "You can't book again because the ride is full now")
        return redirect('my_booking')
    cancelbok.status="active" 
    cancelbok.ride.available_seats-=1 
    cancelbok.ride.save()  
    cancelbok.save() 
    try:                
        subject="Booking Activated again",
        message=f"""Hi {cancelbok.ride.driver.username}, {cancelbok.booked_by.username} has activate his ride again \n\n THANK YOU FOR USING YOUR APP😘"""
        from_mail=f"RideShare <{settings.EMAIL_HOST_USER}>"
        to_mail=[cancelbok.ride.driver.email]   
        send_mail(
            subject=subject, message=message, from_email=from_mail,recipient_list=to_mail 
        ) 
        
    except Exception as e:      
            messages.warning(request,f"error occur {e}") 
            return redirect('my_booking') 
    messages.success(request,'Ride Successfully Activated')
    return redirect('my_booking') 


# deleting btn in my bookings page
def deleteBook(request,id): 
    deletebooking=get_object_or_404(My_booking,id=id,booked_by=request.user) 
    deletebooking.delete()
    return redirect('my_booking') 



# user viewing all his post ride and passengers who booked their ride 
@login_required
def myRides(request):
    # Get all rides posted by the current user
    rides_posted = RidePost.objects.filter(driver=request.user)
    
    # Get all bookings for these rides
    bookings = My_booking.objects.filter(ride__in=rides_posted).select_related('ride', 'booked_by')
    
    # Organize data by ride for better presentation
    # rides_with_bookings = []
    # for ride in rides_posted: 
    #     ride_bookings = bookings.filter(ride=ride)
    #     if ride_bookings.exists():  
    #         rides_with_bookings.append({
    #             'ride': ride,
    #             'bookings': ride_bookings,
    #             'total_passengers': ride_bookings.count(), 
    #             # You could add other aggregated data here
    #         })
    
    context = {
        
        'all_bookings': bookings ,
        'ridesposted':rides_posted
    }

    return render(request, 'my-rides.html', context)



def cancelPostRideBtn(request, id):
    cancelRide = get_object_or_404(RidePost, id=id)
    cancelRide.ride_status = "cancelled"
    cancelRide.save()

    bookings = My_booking.objects.filter(ride=cancelRide, status='active')
    
    # Prepare message list
    mail_list = []
    from_email = f"RideShare <{settings.EMAIL_HOST_USER}>"

    for booking in bookings:
        passenger = booking.booked_by
        subject = " Ride Cancelled"
        message = f"""
        Dear {passenger.username},

        The ride from {cancelRide.departure} to {cancelRide.destination} on {cancelRide.departure_date} at {cancelRide.departure_time} 
        has been CANCELLED by the driver ({cancelRide.driver.username}).

        We're sorry for the inconvenience. Thank you for using RideShare. 😊
        """ 
        mail_list.append((subject, message, from_email, [passenger.email]))

    # Send all mails at once
    try: 
        send_mass_mail(mail_list, fail_silently=False)
        bookings.update(status='cancelled')  
    except Exception as e:
        messages.warning(request, f"Email error: {e}")
        return redirect('my_rides')

    messages.success(request, "Ride cancelled and all passengers notified.")
    return redirect('my_rides')

# activate post btn
def activatePostRideBtn(request, id):
    cancelRide = get_object_or_404(RidePost, id=id)
    cancelRide.ride_status = "active"
    cancelRide.save()

    bookings = My_booking.objects.filter(ride=cancelRide, status='cancelled')
    
    # Prepare message list
    mail_list = []
    from_email = f"RideShare <{settings.EMAIL_HOST_USER}>"

    for booking in bookings:
        passenger = booking.booked_by
        subject = " Ride Activated"
        message = f"""
        Dear {passenger.username},

        The ride from {cancelRide.departure} to {cancelRide.destination} on {cancelRide.departure_date} at {cancelRide.departure_time} 
        has been activated again by the driver ({cancelRide.driver.username}).

        We're sorry for the inconvenience. Thank you for using RideShare. 😊
        """ 
        mail_list.append((subject, message, from_email, [passenger.email]))

    # Send all mails at once
    try: 
        send_mass_mail(mail_list, fail_silently=False)
        bookings.update(status='active')  
    except Exception as e:
        messages.warning(request, f"Email error: {e}")
        return redirect('my_rides')

    messages.success(request, "Ride activated and all passengers notified.")
    return redirect('my_rides')


# delete btn in post myride page
def deletePostRide(request,id):
    deleteride=get_object_or_404(RidePost,id=id) 
    bookings = My_booking.objects.filter(ride=deleteride, status='active')
    deleteride.delete()
    
    # Prepare message list
    mail_list = []
    from_email = f"RideShare <{settings.EMAIL_HOST_USER}>"

    for booking in bookings:
        passenger = booking.booked_by
        subject = " Ride Deleted"
        message = f"""
        Dear {passenger.username},

        The ride from {deleteride.departure} to {deleteride.destination} on {deleteride.departure_date} at {deleteride.departure_time} 
        has been CANCELLED deleted by the driver ({deleteride.driver.username}).

        We're sorry for the inconvenience. Thank you for using RideShare. 😊
        """ 
        mail_list.append((subject, message, from_email, [passenger.email]))

    # Send all mails at once
    try: 
        send_mass_mail(mail_list, fail_silently=False)
    except Exception as e:
        messages.warning(request, f"Email error: {e}")
        return redirect('my_rides')

    messages.info(request,'Ride successfully deleted')
    return redirect('my_rides')

@login_required
def edit_ride(request, id):
    ride = get_object_or_404(RidePost, id=id, driver=request.user)

    if request.method == 'POST':
        form = RidePostForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()

            # Get all users who have booked this ride and their emails
            booked_users = My_booking.objects.filter(ride=ride, status="active")
            recipient_emails = [b.booked_by.email for b in booked_users if b.booked_by.email]

            # Prepare and send email if there are recipients
            if recipient_emails:
                subject = "Ride Updated - RideShare Ghana"
                message = f"""Hello Rider,

                The ride you booked has been updated. Please find the new details below:

                Departure: {ride.departure}
                Destination: {ride.destination}
                Date: {ride.departure_date}
                Time: {ride.departure_time}
                Price: GHS {ride.price_per_seat}
                Driver: {ride.driver.username}

                If you have any concerns, please contact the driver.

                Thank you for using RideShare Ghana 
                """

                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        recipient_emails,
                        fail_silently=False,
                    )
                except Exception as e:
                    messages.warning(request, f"Ride updated, but failed to send emails: {e}")
                    return redirect('my_rides')
            messages.success(request, "Ride updated successfully.")
            return redirect('my_rides')
    else:
        form = RidePostForm(instance=ride)

    return render(request, 'edit_ride.html', {'form': form})


def about(request):
    return render(request,'about.html')


def help(request):
    return render(request,'help.html')

@login_required
def how_it_work(request):
    return render(request,'how-it-works.html')

@login_required
def messages_view(request):
    return render(request,'messages.html')

# def my_ride(request):
#     driver_rides=RidePost.objects.filter(driver=request.user)
#     return render(request, 'my-rides.html', {'myrides':driver_rides})

@login_required
def safety(request):
    return render(request,'safety.html')


def logout_view(request):
    logout(request) 
    return redirect('home') 

# View profile info 
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

# edit profile view 
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  
    else: 
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})


@csrf_exempt
def cron_send_ride_notifications(request,secret_key):
    if secret_key != settings.CRON_SECRET_KEY:
        return HttpResponse("Unauthorized", status=401)
    today = timezone.now().date()

    # Rides scheduled for today
    rides_today = RidePost.objects.filter(departure_date=today, allowed_post=True)

    for ride in rides_today:
        # Notify the driver
        send_mail(
            subject=" Ride Reminder",
            message=f"Hi {ride.driver.username},\n\nYour ride from {ride.departure} to {ride.destination} is scheduled for today at {ride.departure_time}.\n\n- RideShare Ghana",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[ride.driver.email],
            fail_silently=False
        )

        # Notify booked users
        bookings = My_booking.objects.filter(ride=ride, status="active")
        for booking in bookings:
            send_mail(
                subject=" Ride Reminder",
                message=f"Hi {booking.booked_by.username},\n\nReminder: Your ride from {ride.departure} to {ride.destination} is happening today at {ride.departure_time}.\n\n- RideShare Ghana",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[booking.booked_by.email],
                fail_silently=False
            )

        # Optionally notify driver if ride is full
        if ride.available_seats == 0:
            send_mail(
                subject="Your Ride is Full!",
                message=f"Hi {ride.driver.username},\n\nYour ride from {ride.departure} to {ride.destination} is fully booked!\n\n- RideShare Ghana",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[ride.driver.email],
                fail_silently=False
            )

    return HttpResponse("Emails sent.")
