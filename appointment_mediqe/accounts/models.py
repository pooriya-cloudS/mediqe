from django.db import models
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
from django.db import models


# Custom manager for User model
class CustomUserManager(BaseUserManager):
    # Create regular user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    # Create superuser (admin)
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Doctor", "Doctor"),
        ("Patient", "Patient"),
        ("Nurse", "Nurse"),
        ("Receptionist", "Receptionist"),
    ]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # Unique ID
    username = models.CharField(max_length=150)  # Optional username
    email = models.EmailField(unique=True)  # Unique email used for login
    password = models.CharField(max_length=128)  # Hashed password
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="Patient"
    )  # User role
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True
    )  # Optional profile image
    is_active = models.BooleanField(default=True)  # Can log in
    is_verified = models.BooleanField(default=False)  # Email or account verified
    created_at = models.DateTimeField(auto_now_add=True)  # Created timestamp
    extra_info = models.JSONField(null=True, blank=True)  # Optional extra data
    is_staff = models.BooleanField(default=False)  # Can access admin site

    USERNAME_FIELD = "email"  # Use email to log in
    REQUIRED_FIELDS = []  # Required when creating superuser via CLI

    objects = CustomUserManager()  # Connect custom manager

    def __str__(self):
        return self.email  # Show email as string representation


# assuming User is in the same app


class UserProfile(models.Model):
    # Blood type choices
    BLOOD_TYPES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    # One-to-one link to User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    insurance_number = models.CharField(max_length=50)  # User's insurance ID
    insurance_company = models.CharField(max_length=100)  # Insurance provider name
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)  # Blood type

    chronic_conditions = (
        models.TextField()
    )  # Medical conditions (e.g., diabetes, asthma)
    license_number = models.CharField(
        max_length=50
    )  # License number (for doctors/nurses)
    specialty = models.CharField(max_length=50)  # Area of expertise (e.g., cardiology)
    bio = models.TextField()  # Short biography or description

    years_experience = models.IntegerField()  # Years of work experience
    rating = models.FloatField()  # User's rating (e.g., 4.5 out of 5)
    verified = models.BooleanField(default=False)  # Profile verification status

    def __str__(self):
        return f"{self.user.email} Profile"  # String representation of profile
