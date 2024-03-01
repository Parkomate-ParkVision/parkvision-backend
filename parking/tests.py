from django.test import TestCase
from django.contrib.auth import get_user_model
from organization.models import Organization
from parking.models import Parking, CCTV
from uuid import UUID

User = get_user_model()

class ParkingModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test User', phone='+1234567890')
        self.organization = Organization.objects.create(owner=self.user, name='Test Organization', address='123 Test St', entry_gates=2, exit_gates=2, total_slots=100, filled_slots=50, isActive=True)
        self.parking_data = {
            'organization': self.organization,
            'name': 'Test Parking',
            'totalSlots': 50,
            'availableSlots': 25,
            'isActive': True
        }

    def test_create_parking(self):
        parking = Parking.objects.create(**self.parking_data)
        self.assertIsInstance(parking.id, UUID)
        self.assertEqual(parking.organization, self.organization)
        self.assertEqual(parking.name, self.parking_data['name'])
        self.assertEqual(parking.totalSlots, self.parking_data['totalSlots'])
        self.assertEqual(parking.availableSlots, self.parking_data['availableSlots'])
        self.assertTrue(parking.isActive)

class CCTVModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test User', phone='+1234567890')
        self.organization = Organization.objects.create(owner=self.user, name='Test Organization', address='123 Test St', entry_gates=2, exit_gates=2, total_slots=100, filled_slots=50, isActive=True)
        self.parking = Parking.objects.create(organization=self.organization, name='Test Parking', totalSlots=50, availableSlots=25, isActive=True)
        self.cctv_data = {
            'parking': self.parking,
            'name': 'Test CCTV',
            'url': 'http://example.com/stream',
            'isActive': True
        }

    def test_create_cctv(self):
        cctv = CCTV.objects.create(**self.cctv_data)
        self.assertIsInstance(cctv.id, UUID)
        self.assertEqual(cctv.parking, self.parking)
        self.assertEqual(cctv.name, self.cctv_data['name'])
        self.assertEqual(cctv.url, self.cctv_data['url'])
        self.assertTrue(cctv.isActive)
