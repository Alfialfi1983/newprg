from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name= 'home'),
    path('register/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('login/patientdashboard',views.patientdashboard,name='patientdashboard'),
    path('logdoc/',views.LoginDoc, name='logdoc'),
    path('logdoc/doctordashboard', views.doctordashboard, name='doctordashboard'),
    path('bkapp/',views.book_appointment,name='book_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('view-appviadate/', views.view_appviadate, name='view_appviadate'),
    path('logout/', views.LogoutPage, name='logout'),
    path('confirm_appointment/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('reject_appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('user-details/<int:user_id>/', views.user_details, name='user_details'),
    path('appointment_status/', views.appointment_status, name='appointment_status'),
    path('appointment-exists/', views.app_exist, name='app_exist'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('success/', views.success, name='success'),
    path('delete_appointments/', views.delete_appointments, name='delete_appointments'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('add_prescription/<int:user_id>/', views.add_prescription, name='add_prescription'),
    path('user_prescriptions/', views.user_prescriptions, name='user_prescriptions'),
    path('appointments-queue/', views.appointments_queue, name='appointments_position'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),



]
