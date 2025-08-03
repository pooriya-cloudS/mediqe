from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, UserProfile
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserProfileSerializer
)
from django.shortcuts import render


def home_view(request):
    return render(request, 'accounts/home.html')


# === User ViewSet ===
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view or edit user data.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# === User Profile ViewSet ===
class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view or edit user profiles.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


# === Registration API ===
class RegisterAPIView(APIView):
    """
    API endpoint for registering new users.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# === Login API ===
class LoginAPIView(APIView):
    """
    API endpoint for authenticating users and returning tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_id": str(user.id),
                "email": user.email
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



git add .
git commit -m "Initial push: add project files"


