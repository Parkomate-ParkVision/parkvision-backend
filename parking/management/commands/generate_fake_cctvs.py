from django.core.management.base import BaseCommand
from faker import Faker
from parking.models import Parking, CCTV

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake CCTVs'

    def handle(self, *args, **kwargs):
        parkings = Parking.objects.all()

        for parking in parkings:
            for _ in range(2):  # Create 2 CCTVs for each parking
                name = fake.word()
                url = fake.url()

                cctv = CCTV.objects.create(
                    parking=parking,
                    name=name,
                    url=url
                )

                self.stdout.write(self.style.SUCCESS(f'Fake CCTV created for parking: {parking.name}'))
