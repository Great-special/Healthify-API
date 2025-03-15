from django.urls import path
from . import views



urlpatterns = [
    path('submit-email/', views.SubmitEmailView.as_view(), name='submit-email'),
    path('verify-email/<uuid:token>/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('complete-registration/', views.CompleteRegistrationView.as_view(), name='complete-registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uuid:token>/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('create-doctor-profile/', views.create_doctors_profile, name='create_doctor_profile'),
]
