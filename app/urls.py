from django.urls import path
from .import views
from django.contrib.auth import views as auth_views 
from .views import CustomPasswordResetView


urlpatterns=[
    path('',views.index,name='home'),
    path('home',views.index,name='home'),
    path('logout',views.logout_view,name='logout'),
    path('signup',views.signup,name="signup"),
    path('login',views.login_view,name="login"),
    path('about',views.about,name="about"),
    path('find_ride',views.find_ride,name="find_ride"),
    path('help',views.help,name="help"),
    path('how_it_work',views.how_it_work,name="how_it_work"),
    path('messages',views.messages_view,name="messages"),
    path('offer_ride',views.offer_ride,name="offer_ride"),
    path('my_rides',views.myRides,name="my_rides"),
    path('safety',views.safety,name="safety"),
    path('bookbtn<int:id>',views.bookBtn,name="bookbtn"),
    path('cancelbooking<int:id>',views.cancelBokBtn,name="cancelbooking"),
    path('activatebooking<int:id>',views.activateBokBtn,name="activatebooking"),
    path('deletebooking<int:id>',views.deleteBook,name="deletebooking"),
    path('my_booking',views.my_bookings,name="my_booking"), 
    path('cancelRide<int:id>',views.cancelPostRideBtn,name="cancelRide"), 
    path('activeRide<int:id>',views.activatePostRideBtn,name="activeRide"), 
    path('deletePostRide<int:id>',views.deletePostRide,name="deletePostRide"), 
    path('edit-ride/<int:id>/', views.edit_ride, name='edit_ride'),
    path('profile/',views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('cron-notify-rides/<str:secret_key>/', views.cron_send_ride_notifications),

    path('password_reset/',CustomPasswordResetView.as_view(
         template_name='reset_password.html',
         email_template_name="email_reset_password.html", 
         html_email_template_name="email_reset_password.html",
     ),name='password_reset'),  
    
    
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
         template_name="reset_password_done.html",
         
     ),name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
         template_name="reset_password_confirm.html"
     ),name="password_reset_confirm"),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
          template_name="reset_password_complete.html"  
     ),name='password_reset_complete'),

]





