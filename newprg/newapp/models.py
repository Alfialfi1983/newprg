from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)

    # Mobile number validation using RegexValidator
    contact = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Enter a valid mobile number.',
            ),
        ],
    )

    gender = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=GENDER_CHOICES,
    )


class Appointment(models.Model):
    app_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_date = models.DateField()
    TIME_SLOT_CHOICES = [
        ('09:00', '9:00 am'),
        ('09:30', '9:30 am'),
        ('10:00', '10:00 am'),
        ('10:30', '10:30 am'),
        ('11:00', '11.00 am'),
        ('11:30','11:30 am'),
        ('12:00' ,'12:00 pm'),
        ('12:30', '12:30 pm'),
        ('13:00', '1:00 pm'),
    ]
    time_slot = models.CharField(max_length=5, choices=TIME_SLOT_CHOICES)
    description = models.TextField()
    confirm=models.BooleanField(null=True)


    def __str__(self):
        return f"Appointment {self.app_id} - {self.app_date} {self.time_slot}"
#prescription

# models.py


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    next_meeting = models.DateField()

    def __str__(self):
        return f"Prescription {self.prescription_id} - User: {self.user.username}"



