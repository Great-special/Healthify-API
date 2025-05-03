from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import PatientProfileSerializer, DoctorsProfileSerializer
from .models import Appointment
from .serializers import AppointmentSerializer, WalletSerializer, NotificationSerializer


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    return Response({
        "profile": PatientProfileSerializer(request.user.userprofile).data,
        "appointments": AppointmentSerializer(Appointment.objects.filter(user=request.user), many=True).data,
        "wallet": WalletSerializer(Wallet.objects.get(user=request.user)).data,
        "notifications": NotificationSerializer(Notification.objects.filter(user=request.user), many=True).data,
    })


class CreateGetAppointment(APIView):
    permission_classes = []
    
    def post(self, request):     
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        if id:
            try:
                instance = get_object_or_404(Appointment, id=id)
                serializer = AppointmentSerializer(instance)
                return Response(serializer.data)
            except Appointment.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                queryset = Appointment.objects.all()
                serializer = AppointmentSerializer(queryset, many=True)
                return Response(serializer.data)
            except Appointment.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)





