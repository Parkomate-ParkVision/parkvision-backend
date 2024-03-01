from rest_framework.test import APITestCase
from rest_framework import status
from parking.models import Parking, CCTV
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import ParkomateUser
from organization.models import Organization
import warnings
warnings.filterwarnings("ignore")


class ParkingTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+911234567890',
            'password': 'testpassword',
            'is_admin': True,
            'is_staff': True,
            'is_superuser': True,
        }
        self.user = ParkomateUser.objects.create_user(**self.user_data)

        self.organization_data = {
            'name': 'Test Organization',
            'owner': self.user,
        }
        self.organization = Organization.objects.create(**self.organization_data)

        self.parking_data = {
            'name': 'Test Parking',
            'organization': self.organization,
        }
        self.parking = Parking.objects.create(**self.parking_data)

        # Obtain tokens
        login_url = reverse('login')
        response = self.client.post(login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        tokens = response.data.get('tokens')
        self.access_token = tokens.get('access')
        self.refresh_token = tokens.get('refresh')

    def test_parking_list_view(self):
        url = reverse('parkings-list')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parking_detail_view(self):
        url = reverse('parkings-detail', kwargs={'pk': self.parking.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.parking_data.get('name'))

    def test_parking_create_view(self):
        self.parking.delete()
        self.parking_data['organization'] = self.organization.id
        url = reverse('parkings-list')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.post(url, self.parking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_parking_update_view(self):
        url = reverse('parkings-detail', kwargs={'pk': self.parking.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        updated_data = {'name': 'Updated Parking Name', 'organization': self.organization.id}
        response = client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parking_delete_view(self):
        url = reverse('parkings-detail', kwargs={'pk': self.parking.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CCTVTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+911234567890',
            'password': 'testpassword',
            'is_admin': True,
            'is_staff': True,
            'is_superuser': True,
        }
        self.user = ParkomateUser.objects.create_user(**self.user_data)

        self.organization_data = {
            'name': 'Test Organization',
            'owner': self.user,
        }
        self.organization = Organization.objects.create(**self.organization_data)

        self.parking_data = {
            'name': 'Test Parking',
            'organization': self.organization,
        }
        self.parking = Parking.objects.create(**self.parking_data)

        self.cctv_data = {
            'name': 'Test CCTV',
            'parking': self.parking,
        }
        self.cctv = CCTV.objects.create(**self.cctv_data)

        # Obtain tokens
        login_url = reverse('login')
        response = self.client.post(login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        tokens = response.data.get('tokens')
        self.access_token = tokens.get('access')
        self.refresh_token = tokens.get('refresh')

    def test_cctv_list_view(self):
        url = reverse('cctvs-list')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cctv_detail_view(self):
        url = reverse('cctvs-detail', kwargs={'pk': self.cctv.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.cctv_data.get('name'))

    def test_cctv_create_view(self):
        self.cctv.delete()
        self.cctv_data['parking'] = self.parking.id
        url = reverse('cctvs-list')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.post(url, self.cctv_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cctv_update_view(self):
        url = reverse('cctvs-detail', kwargs={'pk': self.cctv.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        updated_data = {'name': 'Updated CCTV Name', 'parking': self.parking.id}
        response = client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cctv_delete_view(self):
        url = reverse('cctvs-detail', kwargs={'pk': self.cctv.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
