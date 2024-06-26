from django.core.management.base import BaseCommand
from faker import Faker
from organization.models import Gate
from parking.models import Parking
from vehicle.models import Vehicle
import random
import multiprocessing
import datetime

fake = Faker()

def create_fake_vehicle(gate):
    for _ in range(15):  # Create 15 vehicles for each gate
        number_plate = "".join(fake.random_letters(length=2)).upper() + str(fake.random_number(digits=4))
        cropped_image = fake.image_url()
        vehicle_image = fake.image_url()
        entry_time = fake.date_time_this_year()
        exit_time = entry_time + datetime.timedelta(minutes=random.randint(30, 360))  # exit_time after entry_time
        randint = random.randint(0, 2)
        vehicle_type = ['economy', 'midrange', 'premium'][randint]
        parking = random.choice(Parking.objects.all())

        vehicle = Vehicle.objects.create(
            number_plate=number_plate,
            cropped_image=cropped_image,
            vehicle_image=vehicle_image,
            entry_gate=gate,
            entry_time=entry_time,
            exit_time=exit_time,
            vehicle_type=vehicle_type,
            parking=parking
        )

        print(f'Fake vehicle created for gate: {gate.id}')

class Command(BaseCommand):
    help = 'Generate fake vehicles'

    def handle(self, *args, **kwargs):
        gates = Gate.objects.all()
        pool_size = multiprocessing.cpu_count()

        pool = multiprocessing.Pool(processes=pool_size)

        for gate in gates:
            pool.apply_async(create_fake_vehicle, args=(gate,))

        pool.close()
        pool.join()
