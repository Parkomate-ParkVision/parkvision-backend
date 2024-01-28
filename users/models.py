from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from dotenv import load_dotenv
load_dotenv()


class ParkomateUserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have email address")
        if not name:
            raise ValueError("Users must have name")
        if not phone:
            raise ValueError("Users must have phone number")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not email:
            raise ValueError("Users must have email address")
        if not name:
            raise ValueError("Users must have name")
        if not phone:
            raise ValueError("Users must have phone number")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class ParkomateUser(AbstractBaseUser, PermissionsMixin):
    PRIVILEGE_CHOICES = (
        (0, 'SUPERUSER'),
        (1, 'ADMIN'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    phone = PhoneNumberField(unique=True)
    profilePicture = models.URLField(
        blank=True, null=True, default="https://img.icons8.com/fluency-systems-regular/96/user--v1.png")
    privilege = models.IntegerField(choices=PRIVILEGE_CHOICES, default=1)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = ParkomateUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        db_table = 'parkomate_user'
