from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()
UserModel = get_user_model()

class Command(BaseCommand):
    help = 'Generate fake users'

    def handle(self, *args, **kwargs):
        number_of_users = 30  # Number of fake users to create

        for _ in range(number_of_users):
            name = fake.name()
            email = fake.email()
            phone = fake.phone_number()

            user = UserModel.objects.create_user(
                email=email,
                name=name,
                phone=phone,
                password='password123'  # You can set a common password for all users or generate random passwords
            )

            self.stdout.write(self.style.SUCCESS(f'Fake user created: {user.email}'))
