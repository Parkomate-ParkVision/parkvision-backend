from django.core.management.base import BaseCommand
from organization.models import Organization, Gate

class Command(BaseCommand):
    help = 'Generate fake gates for organizations'

    def handle(self, *args, **kwargs):
        organizations = Organization.objects.all()

        for organization in organizations:
            for _ in range(2):  # Creating 3 gates for each organization
                gate = Gate.objects.create(organization=organization)

                self.stdout.write(self.style.SUCCESS(f'Fake gate created for organization: {organization.name}'))
