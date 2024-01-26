from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField
from organization.models import Organization
from dotenv import load_dotenv
load_dotenv()


class ParkomateUserManager(BaseUserManager):
    def create_user(self, email, name, organization, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have email address")
        if not name:
            raise ValueError("Users must have name")
        if not organization:
            raise ValueError("Users must have organization id")
        if not phone:
            raise ValueError("Users must have phone number")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            organization=organization,
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
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    privilege = models.IntegerField(choices=PRIVILEGE_CHOICES, default=1)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = ParkomateUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'organization', 'phone']

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'parkomate_user'
