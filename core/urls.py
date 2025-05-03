from django.urls import path

from . import views


urlpatterns = [
    # Appointments
    path('appointments/', views.CreateGetAppointment.as_view(), name='get-appointments'),
    path('appointment/<int:id>/', view=views.CreateGetAppointment.as_view(), name='get-appointment'),
    path('appointment/book/', view=views.CreateGetAppointment.as_view(), name='create-appointment'),
]
