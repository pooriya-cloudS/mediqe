from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
import uuid


# === Custom User Manager === 
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with all permissions.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# === Custom User Model ===
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Patient")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    extra_info = models.JSONField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    # === Avoid reverse accessor conflicts with Django default User ===
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='Groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Permissions specific to this user.',
        verbose_name='user permissions',
    )

    # Use email as the login field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email and password are required by default

    # Use the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

# === User Profile Model ===
class UserProfile(models.Model):
    BLOOD_TYPES = [
        ("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"), ("O+", "O+"), ("O-", "O-"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # Link to custom user
    insurance_number = models.CharField(max_length=50)  # Insurance ID
    insurance_company = models.CharField(max_length=100)  # Name of insurance provider
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)

    chronic_conditions = models.TextField()  # List of medical conditions
    license_number = models.CharField(max_length=50)  # For doctors/nurses
    specialty = models.CharField(max_length=50)  # Medical specialty
    bio = models.TextField()  # Short biography

    years_experience = models.IntegerField()  # Years of experience
    rating = models.FloatField()  # User rating (e.g., 4.5)
    verified = models.BooleanField(default=False)  # Profile verification status

    def __str__(self):
        return f"{self.user.email} Profile"
