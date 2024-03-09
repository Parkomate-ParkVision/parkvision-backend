from django.core.management.base import BaseCommand
from faker import Faker
from vehicle.models import Vehicle
from analytics.models import VehicleDetails
import random
import multiprocessing

fake = Faker()

def create_fake_vehicle_details(vehicle):
    vehicle_class_choices = ['SUV', 'Sedan', 'Hatchback']
    norms_type_choices = ['BS4', 'BS6']
    manufacturer_model_choices = ['Toyota Camry', 'Honda Civic', 'Ford Mustang', 'BMW 3 Series']
    fuel_type_choices = ['Petrol', 'Diesel', 'Electric']
    state_choices = ['California', 'New York', 'Texas', 'Florida']
    insurance_name_choices = ['Geico', 'Progressive', 'State Farm', 'Allstate']

    vehicle_detail = VehicleDetails.objects.create(
        vehicle=vehicle,
        owner_name=fake.name(),
        vehicle_class=random.choice(vehicle_class_choices),
        norms_type=random.choice(norms_type_choices),
        manufacturer_model=random.choice(manufacturer_model_choices),
        insurance_validity=fake.date_between(start_date='-30d', end_date='+365d').strftime('%Y-%m-%d'),
        address=fake.address(),
        seating_capacity=random.randint(2, 7),
        manufacturing_year=fake.year(),
        manufacturer=fake.company(),
        state=random.choice(state_choices),
        fuel_type=random.choice(fuel_type_choices),
        puc_valid_upto=fake.date_between(start_date='-30d', end_date='+365d').strftime('%Y-%m-%d'),
        insurance_name=random.choice(insurance_name_choices)
    )

    print(f'Fake vehicle details created for vehicle: {vehicle}')

class Command(BaseCommand):
    help = 'Generate fake vehicle details'

    def handle(self, *args, **kwargs):
        vehicles = Vehicle.objects.all()
        pool_size = multiprocessing.cpu_count()

        pool = multiprocessing.Pool(processes=pool_size)

        for vehicle in vehicles:
            pool.apply_async(create_fake_vehicle_details, args=(vehicle,))

        pool.close()
        pool.join()
