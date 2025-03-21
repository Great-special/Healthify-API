import uuid
from django.contrib.auth import authenticate
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserEmails, CustomUser
from .serializers import (
    DoctorsProfile, DoctorsProfileSerializer, PatientProfile, UserEmailsSerializer,
    PatientProfileSerializer, PharmacyStoreProfile, PharmacyStoreProfileSerializer,
    CustomUserSerializer, LoginSerializer, ForgotPasswordSerializer, ChangePasswordSerializer,
    ResetPasswordSerializer,
)
from .utility import get_user_from_token



# Create your views here.
class SubmitEmailView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = UserEmailsSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user_email, created = UserEmails.objects.get_or_create(email=email)
            verification_link = request.build_absolute_uri(
                reverse('verify-email', kwargs={'token': user_email.verification_token})
            )
            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {verification_link}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Verification email sent. Please check your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        serializer = UserEmailsSerializer()
        return Response(serializer.data)
    
class VerifyEmailView(APIView):
    permission_classes = []
    def get(self, request, token):
        try:
            user_email = UserEmails.objects.get(verification_token=token)
            if user_email.token_expiration > timezone.now():
                return Response({"message": "Email verified. Please complete your registration."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Verification link expired."}, status=status.HTTP_400_BAD_REQUEST)
        except UserEmails.DoesNotExist:
            return Response({"message": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)

class CompleteRegistrationView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Registration complete. Redirecting to dashboard."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = get_object_or_404(CustomUser, email=email)
            user_auth = authenticate(request, username=user, password=password)
            if user_auth:
                refresh = RefreshToken.for_user(user_auth)
                return Response({
                    "message": "Login successful.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user_email = UserEmails.objects.get(email=email)
                reset_token = uuid.uuid4()
                user_email.verification_token = reset_token
                user_email.token_expiration = timezone.now() + timezone.timedelta(hours=1)
                user_email.save()
                reset_link = request.build_absolute_uri(
                    reverse('reset-password', kwargs={'token': reset_token}))
                send_mail(
                    'Reset your password',
                    f'Click the link to reset your password: {reset_link}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
            except UserEmails.DoesNotExist:
                return Response({"message": "Email not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, token):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_email = UserEmails.objects.get(reset_token=token)
                if user_email.token_expiration > timezone.now():
                    user = CustomUser.objects.get(email=user_email.email)
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
            except UserEmails.DoesNotExist:
                return Response({"message": "Invalid User."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # Keep the user logged in
                return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
            return Response({"message": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def create_doctors_profile(request):
    user = request.user
    if request.method == 'POST':
        serializer = DoctorsProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user) # OR serializer.validated_data['user_id'] = user
        
        return Response(serializer.data)


@api_view()
def get_doctors(request, id=None):
    if id != None:
        try:
            obj = get_object_or_404(DoctorsProfile, id=id)
            print(obj, 'obj')
            serializer = DoctorsProfileSerializer(obj)
            return Response(serializer.data)
        except DoctorsProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            queryset = DoctorsProfile.objects.all()
            serializer = DoctorsProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        except DoctorsProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class CreatePatientProfile(APIView):
    def post(self, request):
        user = request.user
        serializer = PatientProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetPatientProfile(APIView):
    def get(self, request, id=None):
        if id != None:
            try:
                obj = get_object_or_404(PatientProfile, id=id)
                serializer = PatientProfileSerializer(obj)
                return Response(serializer.data)
            except PatientProfile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                queryset = PatientProfile.objects.all()
                serializer = PatientProfileSerializer(queryset, many=True)
                return Response(serializer.data)
            except PatientProfile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

class CreatePharmacyProfile(APIView):
    def post(self, request):
        user = request.user
        serializer = PharmacyStoreProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPharmacyProfile(APIView):
    def get(self, request, id=None):
        try:
            if id != None:
                obj = get_object_or_404(PharmacyStoreProfile, id=id)
                serializer = PharmacyStoreProfileSerializer(obj)
                return Response(serializer.data)
            else:
                queryset = PharmacyStoreProfile.objects.all()
                serializer = PharmacyStoreProfileSerializer(queryset, many=True)
                return Response(serializer.data)
        except PharmacyStoreProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)