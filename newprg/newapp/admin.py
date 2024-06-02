from django.contrib import admin
from .models import Appointment,Prescription,UserProfile



class AppointmentAdmin(admin.ModelAdmin):
   # fields = ['app_id','app_date','time_slot','discription']
   list_display=["app_id","app_date","time_slot","description"]
admin.site.register(Appointment,AppointmentAdmin)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_id', 'user', 'text', 'next_meeting']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'contact', 'gender']

admin.site.register(UserProfile, UserProfileAdmin)
