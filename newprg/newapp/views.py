from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Appointment
from .forms import AppointmentForm,PrescriptionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DateSelectionForm
from .models import Prescription
from datetime import date
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import EditProfileForm, UserProfileForm

# Create your views here.
def home(request):
    return render(request,'index.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('home')

    return render(request, 'signup.html')
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None and not user.is_superuser:
            login(request,user)
            return redirect('patientdashboard')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
def LoginDoc(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None and  user.is_superuser:
            login(request,user)
            return redirect('doctordashboard')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def patientdashboard(request):
    return render(request,'patient_dashboard.html')



def doctordashboard(request):
    return render(request,'doctor_dashboard.html')
#bookappointment
def book_appointment(request):
    existing_appointment = Appointment.objects.filter(user=request.user, confirm=True).first()

    if existing_appointment:
        # If the user already has an existing appointment, pass it to the template
        return render(request, 'app_exist.html', {'existing_appointment': existing_appointment})

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['app_date']
            selected_time_slot = form.cleaned_data['time_slot']

            # Check if the selected time slot is available on the selected date
            existing_appointment_same_slot = Appointment.objects.filter(
                app_date=selected_date,
                time_slot=selected_time_slot
            ).exists()

            if existing_appointment_same_slot:
                messages.error(request, "The selected time slot is not available for this date.")
            elif selected_date < timezone.now().date():
                messages.error(request, "You cannot book an appointment on a past date.")
            else:
                form.instance.user = request.user
                form.save()
                messages.success(request, "Appointment booked successfully!")
                return redirect('patientdashboard')  # Redirect to a success page or another appropriate view
    else:
        form = AppointmentForm()

    return render(request, 'bookapp.html', {'form': form})

#appointmentesisst
def app_exist(request):
    return render(request,'app_exist.html')
#view appointment
def view_appointments(request):
    # Filter appointments that are not confirmed or rejected
    appointments = Appointment.objects.filter(confirm__isnull=True)
    return render(request, 'view_appointments.html', {'appointments': appointments})
#viewappointment_datevice




def view_appviadate(request):
    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['selected_date']

            # Filter appointments by date, confirmed status, and order by time_slot
            appointments = Appointment.objects.filter(
                app_date=selected_date,
                confirm=True
            ).order_by('time_slot')

            return render(request, 'appointments_list.html', {'appointments': appointments, 'selected_date': selected_date})
    else:
        form = DateSelectionForm()

    return render(request, 'select_date.html', {'form': form})

#logout
def LogoutPage(request):
    logout(request)
    return redirect('home')

#confirm and reject appointmnet

def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, app_id=appointment_id)
    #notification
    #user = appointment.user
    #message_text = f"Your appointment on {appointment.app_date} at {appointment.time_slot} has been confirmed."
    #messages.success(request, message_text)
    # Your confirmation logic here (update appointment status, send notifications, etc.)
    appointment.confirm = True  # Assuming 'confirm' is a BooleanField
    appointment.save()

    return redirect('view_appointments')


def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, app_id=appointment_id)

    # Your rejection logic here (update appointment status, send notifications, etc.)
    appointment.delete()
    return redirect('view_appointments')

#userdetails

def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    prescriptions = Prescription.objects.filter(user=user)

    context = {
        'user': user,
        'prescriptions': prescriptions,
    }

    return render(request, 'user_details.html', context)


@login_required
def appointment_status(request):
    user_appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointment_status.html', {'appointments': user_appointments})

#view_prescription


# views.py

#delete appointment
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, app_id=appointment_id)

    # Your rejection logic here (update appointment status, send notifications, etc.)
    appointment.delete()
    return redirect('success')

def success(request):
    return render(request,'success.html')
def delete_appointments(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')

        # Delete appointments for the selected date
        Appointment.objects.filter(app_date=selected_date).delete()

        # Redirect to the same page or a different page as needed
        return redirect('doctordashboard')  # Change 'your_redirect_url' to the desired URL

    return render(request, 'doctor_dashboard.html')

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if request.user != appointment.user:
        messages.error(request, "You do not have permission to cancel this appointment.")
        return redirect('patientdashboard')

    appointment.delete()
    messages.success(request, "Appointment canceled successfully!")
    return redirect('patientdashboard')

#prescriptionadding
def add_prescription(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.user = user
            prescription.save()
            return redirect('user_details', user_id=user.id)

    # If the form is not valid or the request method is not POST
    return redirect('user_details', user_id=user.id)

#view_presc
def user_prescriptions(request):
    # Retrieve prescriptions for the current user
    prescriptions = Prescription.objects.filter(user=request.user)

    context = {
        'prescriptions': prescriptions,
    }

    return render(request, 'presription_user.html', context)
#queue
def appointments_queue(request):
    # Get the logged-in user's upcoming appointment
    user_appointment = Appointment.objects.filter(user=request.user, confirm=True, app_date__gte=date.today()).first()

    if user_appointment:
        # Display appointments only for the user's appointment date
        appointments = Appointment.objects.filter(app_date=user_appointment.app_date, confirm=True).order_by('time_slot')
        return render(request, 'appointments_queue.html',
                      {'appointments': appointments, 'selected_date': user_appointment.app_date})
    else:
        # No upcoming appointment for the user
        return render(request, 'no_appointment.html')

# views.py




@login_required
def edit_profile(request):
    user = request.user

    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        # If UserProfile does not exist, create one
        user_profile = UserProfile(user=user)
        user_profile.save()

    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to the profile page after saving changes
    else:
        user_form = EditProfileForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    user = request.user
    user_profile = user.userprofile  # Assuming you have a UserProfile model associated with the User model

    return render(request, 'profile.html', {'user': user, 'user_profile': user_profile})