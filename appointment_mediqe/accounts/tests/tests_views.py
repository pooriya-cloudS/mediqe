from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from django.contrib.auth import get_user_model


class UserRegistrationAPITest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')  # Make sure this name is correct in urls.py
        self.valid_user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "role": "Patient",
            "first_name": "Test",
            "last_name": "User",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
            "phone": "1234567890",
            "address": "123 Street",
        }

    def test_register_user_successfully(self):
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User registered successfully")
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_register_user_missing_required_fields(self):
        incomplete_data = self.valid_user_data.copy()
        del incomplete_data['email']  # remove email to simulate error
        response = self.client.post(self.register_url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)



class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('login_api')  
        self.user_password = 'testpass123'
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password=self.user_password,
            username='testuser',
            role='Patient',
            first_name='Test',
            last_name='User',
            date_of_birth='1990-01-01',
            gender='Male',
            phone='1234567890',
            address='Test address'
        )

    def test_login_success(self):
        data = {
            'email': 'testuser@example.com',
            'password': self.user_password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_login_wrong_password(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
