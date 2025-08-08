from rest_framework import serializers
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']  # Exclude password from being displayed

    def create(self, validated_data):
        # Pop the password and hash it manually
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Handle password hashing and updating other fields
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested user serializer

    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        # Extract nested user data and create both user and profile
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        # Update both profile and nested user
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
