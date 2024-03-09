from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import multiprocessing

fake = Faker()
UserModel = get_user_model()

def generate_fake_user(name, email, phone):
    user = UserModel.objects.create_user(
        email=email,
        name=name,
        phone=phone,
        password='password123'  # You can set a common password for all users or generate random passwords
    )
    print(f'Fake user created: {user.email}')

class Command(BaseCommand):
    help = 'Generate fake users'

    def handle(self, *args, **kwargs):
        number_of_users = 100  # Number of fake users to create
        pool_size = multiprocessing.cpu_count()  # Number of processes to create

        pool = multiprocessing.Pool(processes=pool_size)

        for _ in range(number_of_users):
            name = fake.name()
            email = fake.email()
            phone = fake.phone_number()

            pool.apply_async(generate_fake_user, args=(name, email, phone))

        pool.close()
        pool.join()
