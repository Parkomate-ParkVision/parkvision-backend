from django.core.management.base import BaseCommand
from organization.models import Organization, Gate
import multiprocessing

class Command(BaseCommand):
    help = 'Generate fake gates for organizations'

    def handle(self, *args, **kwargs):
        organizations = Organization.objects.all()
        pool_size = multiprocessing.cpu_count()

        pool = multiprocessing.Pool(processes=pool_size)

        for organization in organizations:
            for _ in range(2):  # Creating 3 gates for each organization
                pool.apply_async(create_fake_gate, args=(organization,))

        pool.close()
        pool.join()

def create_fake_gate(organization):
    gate = Gate.objects.create(organization=organization)
    print(f'Fake gate created for organization: {organization.name}')
