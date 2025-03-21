import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator


class UserEmails(models.Model):
    email = models.EmailField(unique=True)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    token_expiration = models.DateTimeField()

    def __str__(self):
        return f"{self.email}"
    
    def save(self, *args, **kwargs):
        self.token_expiration = timezone.now() + timezone.timedelta(hours=24)
        return super().save()


class CustomUser(AbstractUser):
    DOCTOR = 'doctor'
    PATIENT = 'patient'
    PHARMACY = 'pharmacy_store'
    
    Types = (
        (DOCTOR, ' Doctor'),
        (PATIENT, 'Patient'),
        (PHARMACY, 'Pharmacy Store')
    )
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    user_type = models.CharField(max_length=100, choices=Types, default=PATIENT)
    
    def __str__(self) -> str:
        return super().__str__()


class DoctorsProfile(models.Model):
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctors_profile')
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.CharField(max_length=100)
    specializations = models.CharField(max_length=100)
    medical_license_number = models.CharField(max_length=100)
    practice_address = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    government_id = models.ImageField(upload_to='government_ids/', blank=True, null=True)
    medical_certificate = models.FileField(upload_to='medical_certificates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
   

    def __str__(self) -> str:
        return self.user_id.username
    
    def get_image(self):
        return self.profile_picture.url if self.profile_picture else None
    


class PatientProfile(models.Model):    
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    portfolio = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=15, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    past_medical_diagnosis = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    weight = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    emergency_contact_information = models.CharField(max_length=100, blank=True, null=True)
    medical_history_reports = models.FileField(upload_to='medical_history_reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.user_id.username
    
    def get_image(self):
        return self.profile_picture.url if self.profile_picture else None
    
    


class PharmacyStoreProfile(models.Model):
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='pharmacy_store')
    name = models.CharField(
        ('Pharmacy Name'), 
        max_length=200, 
        unique=True
    )
    registration_number = models.CharField(
        ('Pharmacy Registration Number'), 
        max_length=50, 
        unique=True
    )
    
    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message=("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )
    phone_number = models.CharField(
        ('Contact Phone'), 
        validators=[phone_regex], 
        max_length=16, 
        blank=True
    )
        
    # Address Details
    address_line1 = models.CharField(
        ('Address Line 1'),
        max_length=255,  
    )
    address_line2 = models.CharField(
        ('Address Line 2'), 
        max_length=255, 
        blank=True, 
        null=True
    )
    city = models.CharField(
        ('City'), 
        max_length=100
    )
    state_province = models.CharField(
        ('State/Province'), 
        max_length=100
    )
    postal_code = models.CharField(
        ('Postal Code'), 
        max_length=20
    )
    country = models.CharField(
        ('Country'), 
        max_length=100
    )
    tax_identification_number = models.CharField(
        ('Tax Identification Number'), 
        max_length=50, 
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)