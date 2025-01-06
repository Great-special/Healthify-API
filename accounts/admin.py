from django.contrib import admin
from .models import CustomUser, DoctorsProfile, PatientProfile
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(DoctorsProfile)
admin.site.register(PatientProfile)