from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers 
from .models import DoctorsProfile, PatientProfile, PharmacyStoreProfile, UserEmails

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'full_name', 'gender', 'password', 'confirm_password', 'user_type']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        if data['full_name']:
            full_name_list = data['full_name'].split()
            data['first_name'] = full_name_list[0]
            data['last_name'] = full_name_list[-1]
            print(data)
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data.pop('full_name')
        user = User.objects.create_user(**validated_data)
        return user
    
# class CustomUserCreateSerializer(UserCreateSerializer):
#     class Meta(UserCreateSerializer.Meta):
#         model = User
#         fields = ('id', 'email', 'username', 'password')

# class CustomUserSerializer(UserSerializer):
#     class Meta(UserSerializer.Meta):
#         model = User
#         fields = ('id', 'email', 'username')
        
class UserEmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmails
        fields = ('id', 'email')
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class DoctorsProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DoctorsProfile
        fields = "__all__"


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = "__all__"
        
class PharmacyStoreProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyStoreProfile
        fields = "__all__"