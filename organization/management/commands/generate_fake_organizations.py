from django.core.management.base import BaseCommand
from faker import Faker
from organization.models import Organization
from users.models import ParkomateUser

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake organizations'

    def handle(self, *args, **kwargs):
        number_of_organizations = 30

        for _ in range(number_of_organizations):
            name = fake.company()
            address = fake.address()
            entry_gates = fake.random_int(min=1, max=10)
            exit_gates = fake.random_int(min=1, max=10)
            total_slots = fake.random_int(min=50, max=500)
            filled_slots = fake.random_int(min=0, max=total_slots)
            owner = ParkomateUser.objects.get(email="admin@admin.com")
            admins = [email for email in ParkomateUser.objects.values_list('email', flat=True)]

            organization = Organization.objects.create(
                name=name,
                address=address,
                entry_gates=entry_gates,
                exit_gates=exit_gates,
                total_slots=total_slots,
                filled_slots=filled_slots,
                owner=owner,
                admins=admins
            )

            self.stdout.write(self.style.SUCCESS(f'Fake organization created: {organization.name}'))
