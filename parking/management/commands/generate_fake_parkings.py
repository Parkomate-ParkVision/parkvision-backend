from django.core.management.base import BaseCommand
from faker import Faker
from organization.models import Organization
from parking.models import Parking

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake parkings'

    def handle(self, *args, **kwargs):
        organizations = Organization.objects.all()

        for organization in organizations:
            for _ in range(10):  # Create 10 parkings for each organization
                name = fake.word()
                total_slots = fake.random_int(min=50, max=500)
                available_slots = fake.random_int(min=0, max=total_slots)

                parking = Parking.objects.create(
                    organization=organization,
                    name=name,
                    totalSlots=total_slots,
                    availableSlots=available_slots
                )

                self.stdout.write(self.style.SUCCESS(f'Fake parking created for organization: {organization.name}'))
