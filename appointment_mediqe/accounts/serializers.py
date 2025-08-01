from rest_framework import serializers
from .models import User, UserProfile


# User serializer for displaying user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']  # Don't expose hashed password


# Serializer for registering new users
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'role', 'first_name', 'last_name',
            'date_of_birth', 'gender', 'phone', 'address', 'avatar', 'extra_info'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# Serializer for the user profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
