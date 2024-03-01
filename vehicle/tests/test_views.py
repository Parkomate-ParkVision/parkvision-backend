from rest_framework.test import APITestCase
from rest_framework import status
from vehicle.models import Vehicle
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import ParkomateUser
from parking.models import Parking
from vehicle.models import Gate
from organization.models import Organization
from copy import deepcopy
import warnings
warnings.filterwarnings("ignore")


class VehicleTestCase(APITestCase):
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

        self.gate_data = {
            'organization': self.organization,
        }
        self.entry_gate = Gate.objects.create(**self.gate_data)
        self.exit_gate = Gate.objects.create(**self.gate_data)

        self.vehicle_data = {
            'vehicle_type': 'economy',
            'parking': self.parking,
            'number_plate': 'ABC123',
            'entry_gate': self.entry_gate,
            'exit_gate': self.exit_gate,
        }
        self.vehicle = Vehicle.objects.create(**self.vehicle_data)

        # Obtain tokens
        login_url = reverse('login')
        response = self.client.post(login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        tokens = response.data.get('tokens')
        self.access_token = tokens.get('access')
        self.refresh_token = tokens.get('refresh')

    def test_vehicle_list_view(self):
        url = reverse('vehicles-list')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vehicle_detail_view(self):
        url = reverse('vehicles-detail', kwargs={'pk': self.vehicle.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('number_plate'), self.vehicle_data.get('number_plate'))

    def test_vehicle_create_view(self):
        self.vehicle.delete()
        data = deepcopy(self.vehicle_data)
        data['entry_gate'] = self.entry_gate.id
        data['exit_gate'] = self.exit_gate.id
        data['parking'] = self.parking.id
        url = reverse('vehicles-list')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vehicle_update_view(self):
        url = reverse('vehicles-detail', kwargs={'pk': self.vehicle.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        updated_data = {'number_plate': 'XYZ789'}
        response = client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vehicle_delete_view(self):
        url = reverse('vehicles-detail', kwargs={'pk': self.vehicle.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unverified_vehicle_view(self):
        url = reverse('unverified-vehicles')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verification_view(self):
        url = reverse('verify-vehicle', kwargs={'pk': self.vehicle.id, 'number_plate': self.vehicle.number_plate})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vehicle_by_organization_view(self):
        url = reverse('organization-vehicles', kwargs={'organization_id': self.organization.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)