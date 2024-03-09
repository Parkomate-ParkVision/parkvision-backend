from django.core.management.base import BaseCommand
from faker import Faker
from organization.models import Organization
from users.models import ParkomateUser
import multiprocessing

fake = Faker()

def generate_fake_organization(name, address, entry_gates, exit_gates, total_slots, filled_slots, parking_threshold, occupancy_limit, hourly_rate, penalty_charges, owner_email):
    owner = ParkomateUser.objects.get(email=owner_email)
    admins = [email for email in ParkomateUser.objects.values_list('email', flat=True)]

    organization = Organization.objects.create(
        owner=owner,
        admins=admins,
        name=name,
        address=address,
        entry_gates=entry_gates,
        exit_gates=exit_gates,
        total_slots=total_slots,
        filled_slots=filled_slots,
        parking_threshold=parking_threshold,
        occupancy_limit=occupancy_limit,
        hourly_rate=hourly_rate,
        penalty_charges=penalty_charges
    )

    print(f'Fake organization created: {organization.name}')

class Command(BaseCommand):
    help = 'Generate fake organizations'

    def handle(self, *args, **kwargs):
        number_of_organizations = 100
        pool_size = multiprocessing.cpu_count()

        pool = multiprocessing.Pool(processes=pool_size)

        for _ in range(number_of_organizations):
            name = fake.company()
            address = fake.address()
            entry_gates = fake.random_int(min=1, max=10)
            exit_gates = fake.random_int(min=1, max=10)
            total_slots = fake.random_int(min=50, max=500)
            filled_slots = fake.random_int(min=0, max=total_slots)
            parking_threshold = fake.random_int(min=1, max=60)
            occupancy_limit = fake.random_int(min=1, max=1440)  # 1 to 1440 minutes (1 day)
            hourly_rate = fake.random_number(digits=2)
            penalty_charges = fake.random_number(digits=2)
            owner_email = "admin@admin.com"

            pool.apply_async(generate_fake_organization, args=(name, address, entry_gates, exit_gates, total_slots, filled_slots, parking_threshold, occupancy_limit, hourly_rate, penalty_charges, owner_email))

        pool.close()
        pool.join()
