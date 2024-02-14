from django.core.management.base import BaseCommand
from faker import Faker
from organization.models import Gate
from vehicle.models import Vehicle

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake vehicles'

    def handle(self, *args, **kwargs):
        gates = Gate.objects.all()

        for gate in gates:
            for _ in range(5):  # Create 5 vehicles for each gate
                number_plate = "".join(fake.random_letters(length=2)).upper() + str(fake.random_number(digits=4))
                cropped_image = fake.image_url()
                vehicle_image = fake.image_url()
                prediction = fake.word()
                entry_time = fake.date_time_this_year()

                vehicle = Vehicle.objects.create(
                    number_plate=number_plate,
                    cropped_image=cropped_image,
                    vehicle_image=vehicle_image,
                    prediction=prediction,
                    entry_gate=gate,
                    entry_time=entry_time
                )

                self.stdout.write(self.style.SUCCESS(f'Fake vehicle created for gate: {gate.id}'))
