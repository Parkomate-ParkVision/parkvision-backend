from rest_framework.test import APITestCase
from rest_framework import status
from organization.models import Organization
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import ParkomateUser
import warnings
warnings.filterwarnings("ignore")


class OrganizationTestCase(APITestCase):
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

        # Obtain tokens
        login_url = reverse('login')
        response = self.client.post(login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        tokens = response.data.get('tokens')
        self.access_token = tokens.get('access')
        self.refresh_token = tokens.get('refresh')

    def test_organization_list_view(self):
        url = reverse('organizations-list')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_organization_detail_view(self):
        url = reverse('organizations-detail', kwargs={'pk': self.organization.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.organization_data.get('name'))

    def test_organization_create_view(self):
        self.organization.delete()
        self.organization_data['owner'] = self.user.id
        url = reverse('organizations-list')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.post(url, self.organization_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_organization_update_view(self):
        url = reverse('organizations-detail', kwargs={'pk': self.organization.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        updated_data = {'name': 'Updated Organization Name'}
        response = client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_organization_delete_view(self):
        url = reverse('organizations-detail', kwargs={'pk': self.organization.id})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)