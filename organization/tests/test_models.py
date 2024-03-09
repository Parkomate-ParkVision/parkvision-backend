from django.test import TestCase
from django.contrib.auth import get_user_model
from organization.models import Organization, Gate
from uuid import UUID

User = get_user_model()

from django.test import TestCase
from organization.models import Organization
from users.models import ParkomateUser


class OrganizationModelTestCase(TestCase):
    def setUp(self):
        self.user = ParkomateUser.objects.create(email='test@example.com', name='Test User', phone='+1234567890')
        self.organization_data = {
            'owner': self.user,
            'admins': ['admin1@example.com', 'admin2@example.com'],
            'name': 'Test Organization',
            'address': '123 Test St',
            'entry_gates': 2,
            'exit_gates': 2,
            'total_slots': 100,
            'filled_slots': 50,
            'parking_threshold': 60,
            'occupancy_limit': 120,
            'hourly_rate': 10.5,
            'penalty_charges': 20.0,
            'isActive': True
        }

    def test_create_organization(self):
        organization = Organization.objects.create(**self.organization_data)
        self.assertEqual(organization.owner, self.user)
        self.assertEqual(list(organization.admins), self.organization_data['admins'])
        self.assertEqual(organization.name, self.organization_data['name'])
        self.assertEqual(organization.address, self.organization_data['address'])
        self.assertEqual(organization.entry_gates, self.organization_data['entry_gates'])
        self.assertEqual(organization.exit_gates, self.organization_data['exit_gates'])
        self.assertEqual(organization.total_slots, self.organization_data['total_slots'])
        self.assertEqual(organization.filled_slots, self.organization_data['filled_slots'])
        self.assertEqual(organization.parking_threshold, self.organization_data['parking_threshold'])
        self.assertEqual(organization.occupancy_limit, self.organization_data['occupancy_limit'])
        self.assertEqual(organization.hourly_rate, self.organization_data['hourly_rate'])
        self.assertEqual(organization.penalty_charges, self.organization_data['penalty_charges'])
        self.assertTrue(organization.isActive)


class GateModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test User', phone='+1234567890')
        self.organization = Organization.objects.create(owner=self.user, name='Test Organization', address='123 Test St', entry_gates=2, exit_gates=2, total_slots=100, filled_slots=50, isActive=True)
        self.gate_data = {
            'organization': self.organization
        }

    def test_create_gate(self):
        gate = Gate.objects.create(**self.gate_data)
        self.assertIsInstance(gate.id, UUID)
        self.assertEqual(gate.organization, self.organization)
