from django.test import TestCase
from vehicle.models import Vehicle
from analytics.models import VehicleDetails
from uuid import UUID

class VehicleDetailsModelTestCase(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(number_plate='ABC123')
        self.vehicle_details_data = {
            'vehicle': self.vehicle,
            'owner_name': 'John Doe',
            'vehicle_class': 'SUV',
            'norms_type': 'BS6',
            'manufacturer_model': 'Toyota Camry',
            'insurance_validity': '2023-12-31',
            'address': '123 Test St',
            'seating_capacity': 5,
            'manufacturing_year': '2022',
            'manufacturer': 'Toyota',
            'state': 'California',
            'fuel_type': 'Petrol',
            'puc_valid_upto': '2023-12-31',
            'insurance_name': 'ABC Insurance'
        }

    def test_create_vehicle_details(self):
        vehicle_details = VehicleDetails.objects.create(**self.vehicle_details_data)
        self.assertIsInstance(vehicle_details.id, UUID)
        self.assertEqual(vehicle_details.vehicle, self.vehicle)
        self.assertEqual(vehicle_details.owner_name, self.vehicle_details_data['owner_name'])
        self.assertEqual(vehicle_details.vehicle_class, self.vehicle_details_data['vehicle_class'])
        self.assertEqual(vehicle_details.norms_type, self.vehicle_details_data['norms_type'])
        self.assertEqual(vehicle_details.manufacturer_model, self.vehicle_details_data['manufacturer_model'])
        self.assertEqual(vehicle_details.insurance_validity, self.vehicle_details_data['insurance_validity'])
        self.assertEqual(vehicle_details.address, self.vehicle_details_data['address'])
        self.assertEqual(vehicle_details.seating_capacity, self.vehicle_details_data['seating_capacity'])
        self.assertEqual(vehicle_details.manufacturing_year, self.vehicle_details_data['manufacturing_year'])
        self.assertEqual(vehicle_details.manufacturer, self.vehicle_details_data['manufacturer'])
        self.assertEqual(vehicle_details.state, self.vehicle_details_data['state'])
        self.assertEqual(vehicle_details.fuel_type, self.vehicle_details_data['fuel_type'])
        self.assertEqual(vehicle_details.puc_valid_upto, self.vehicle_details_data['puc_valid_upto'])
        self.assertEqual(vehicle_details.insurance_name, self.vehicle_details_data['insurance_name'])
