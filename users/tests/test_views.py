from rest_framework.test import APITestCase
from rest_framework import status
from users.models import ParkomateUser
from django.urls import reverse
from rest_framework.test import APIClient
import warnings
warnings.filterwarnings("ignore")


class ParkomateUserTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'name': 'Test User',
            'phone': '+911234567890',
            'email': 'test@example.com',
            'password': 'Test12345'  # assuming a valid password
        }
        self.user = ParkomateUser.objects.create_user(**self.user_data)

        # Obtain tokens
        login_url = reverse('login')
        response = self.client.post(login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        tokens = response.data.get('tokens')
        self.access_token = tokens.get('access')
        self.refresh_token = tokens.get('refresh')

    def test_parkomate_user_register_view(self):
        user = ParkomateUser.objects.get(email=self.user_data.get('email'))
        user.delete()
        url = reverse('register')
        client = APIClient()
        response = client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_parkomate_user_login_view(self):
        url = reverse('login')
        client = APIClient()
        response = client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parkomate_user_list_view(self):
        url = reverse('users-list')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], ParkomateUser.objects.count())

    def test_parkomate_user_detail_view(self):
        url = reverse('users-detail', kwargs={'pk': self.user.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.user_data.get('email'))

    def test_parkomate_user_logout_view(self):
        url = reverse('logout')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        data = {
            "refresh": self.refresh_token
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)