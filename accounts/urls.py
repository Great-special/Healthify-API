from django.urls import path
from . import views



urlpatterns = [
    # User Registration
    path('submit-email/', views.SubmitEmailView.as_view(), name='submit-email'),
    path('verify-email/<uuid:token>/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('complete-registration/', views.CompleteRegistrationView.as_view(), name='complete-registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uuid:token>/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    # Doctor Profile
    path('create-doctor-profile/', views.create_doctors_profile, name='create-doctor-profile'),
    path('update-doctor/<int:id>/', views.update_doctors_profile, name='update-doctor-profile'),
    path('delete-account/<int:id>/', views.delete_doctors_profile, name='delete-doctors-profile'),
    path('get-doctors/<int:id>/', views.get_doctors, name='get-doctors'),
    path('get-doctors/<str:specialization>/', views.get_doctors_specialization, name='get-doctors-specialization'),
    path('get-doctors/', views.get_doctors, name='get-doctors'),

    # Patient Profile
    path('create-patient-profile/', views.CreatePatientProfile.as_view(), name='create-patient-profile'),
    path('update-patient/<int:id>/', views.UpdatePatientProfile.as_view(), name='update-patient-profile'),
    path('delete-patient/<int:id>/', views.DeletePatientProfile.as_view(), name='delete-patient-profile'),
    path('get-patients/', views.GetPatientProfile.as_view(), name='get-patients'), 
    path('get-patients/<int:id>/', views.GetPatientProfile.as_view(), name='get-patients'),
    
    
    # Pharmacy Store Profile
    path('create-pharmacy-profile/', views.CreatePharmacyProfile.as_view(), name='create-pharmacy-profile'),
    path('get-pharmacy-stores/', views.GetPharmacyProfile.as_view(), name='get-pharmacy-stores'),
    path('get-pharmacy-stores/<int:id>/', views.GetPharmacyProfile.as_view(), name='get-pharmacy-stores'),
]
