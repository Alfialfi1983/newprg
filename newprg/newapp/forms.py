from django import forms
from .models import Appointment,Prescription
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile,User
#createappointment
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['app_date', 'time_slot', 'description']

#viewappointment

#eviewdateapp

class DateSelectionForm(forms.Form):
    selected_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

#editpatieent
#loginpatient

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['text', 'next_meeting']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'next_meeting': forms.DateInput(attrs={'type': 'date'}),
        }

# forms.p


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'contact', 'gender']
