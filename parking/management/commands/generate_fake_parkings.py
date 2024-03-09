from django.core.management.base import BaseCommand
from faker import Faker
from organization.models import Organization
from parking.models import Parking
import multiprocessing

fake = Faker()

def create_fake_parking(organization):
    for _ in range(30):  # Create 30 parkings for each organization
        name = fake.word()
        total_slots = fake.random_int(min=50, max=500)
        available_slots = fake.random_int(min=0, max=total_slots)

        parking = Parking.objects.create(
            organization=organization,
            name=name,
            totalSlots=total_slots,
            availableSlots=available_slots
        )

        print(f'Fake parking created for organization: {organization.name}')

class Command(BaseCommand):
    help = 'Generate fake parkings'

    def handle(self, *args, **kwargs):
        organizations = Organization.objects.all()
        pool_size = multiprocessing.cpu_count()

        pool = multiprocessing.Pool(processes=pool_size)

        for organization in organizations:
            pool.apply_async(create_fake_parking, args=(organization,))

        pool.close()
        pool.join()
