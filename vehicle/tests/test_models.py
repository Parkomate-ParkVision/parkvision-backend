from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from organization.models import Gate
from parking.models import Parking
from organization.models import Organization
from vehicle.models import Vehicle
from uuid import UUID

User = get_user_model()

class VehicleModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test User', phone='+1234567890')
        self.organization = Organization.objects.create(owner=self.user, name='Test Organization', address='123 Test St', entry_gates=2, exit_gates=2, total_slots=100, filled_slots=50, isActive=True)
        self.parking = Parking.objects.create(organization=self.organization, name='Test Parking', totalSlots=50, availableSlots=25, isActive=True)
        self.entry_gate = Gate.objects.create(organization=self.organization)
        self.exit_gate = Gate.objects.create(organization=self.organization)
        self.vehicle_data = {
            'vehicle_type': 'economy',
            'parking': self.parking,
            'number_plate': 'ABC123',
            'cropped_image': 'http://example.com/cropped_image.jpg',
            'vehicle_image': 'http://example.com/vehicle_image.jpg',
            'entry_gate': self.entry_gate,
            'exit_gate': self.exit_gate,
            'entry_time': timezone.now(),
            'exit_time': timezone.now(),
            'verified_by': self.user,
            'verified_number_plate': 'ABC123'
        }

    def test_create_vehicle(self):
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        self.assertIsInstance(vehicle.id, UUID)
        self.assertEqual(vehicle.vehicle_type, self.vehicle_data['vehicle_type'])
        self.assertEqual(vehicle.parking, self.vehicle_data['parking'])
        self.assertEqual(vehicle.number_plate, self.vehicle_data['number_plate'])
        self.assertEqual(vehicle.cropped_image, self.vehicle_data['cropped_image'])
        self.assertEqual(vehicle.vehicle_image, self.vehicle_data['vehicle_image'])
        self.assertEqual(vehicle.entry_gate, self.vehicle_data['entry_gate'])
        self.assertEqual(vehicle.exit_gate, self.vehicle_data['exit_gate'])
        self.assertEqual(vehicle.entry_time, self.vehicle_data['entry_time'])
        self.assertEqual(vehicle.exit_time, self.vehicle_data['exit_time'])
        self.assertEqual(vehicle.verified_by, self.vehicle_data['verified_by'])
        self.assertEqual(vehicle.verified_number_plate, self.vehicle_data['verified_number_plate'])
