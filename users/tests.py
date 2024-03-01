from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import ParkomateUser

User = get_user_model()

class ParkomateUserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+911234567890',
            'password': 'testpassword',
            'is_admin': False,
            'is_staff': False,
            'is_superuser': False,
        }

    def test_create_user(self):
        user = ParkomateUser.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.name, self.user_data['name'])
        self.assertEqual(user.phone, self.user_data['phone'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = ParkomateUser.objects.create_superuser(**self.user_data)
        self.assertEqual(superuser.email, self.user_data['email'])
        self.assertEqual(superuser.name, self.user_data['name'])
        self.assertEqual(superuser.phone, self.user_data['phone'])
        self.assertTrue(superuser.check_password(self.user_data['password']))
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_string_representation(self):
        user = ParkomateUser.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['name'])

    def test_user_tokens(self):
        user = ParkomateUser.objects.create_user(**self.user_data)
        tokens = user.tokens()
        self.assertIn('refresh', tokens)
        self.assertIn('access', tokens)
