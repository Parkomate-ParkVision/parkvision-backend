from django.core.management.base import BaseCommand
from faker import Faker
from parking.models import Parking, CCTV
import multiprocessing

fake = Faker()

def create_fake_cctv(parking):
    for _ in range(5):  # Create 5 CCTVs for each parking
        name = fake.word()
        url = fake.url()

        cctv = CCTV.objects.create(
            parking=parking,
            name=name,
            url=url
        )

        print(f'Fake CCTV created for parking: {parking.name}')

class Command(BaseCommand):
    help = 'Generate fake CCTVs'

    def handle(self, *args, **kwargs):
        parkings = Parking.objects.all()
        pool_size = multiprocessing.cpu_count()

        pool = multiprocessing.Pool(processes=pool_size)

        for parking in parkings:
            pool.apply_async(create_fake_cctv, args=(parking,))

        pool.close()
        pool.join()
