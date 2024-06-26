# Generated by Django 4.2.7 on 2024-02-12 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('entry_gates', models.IntegerField(blank=True, null=True)),
                ('exit_gates', models.IntegerField(blank=True, null=True)),
                ('total_slots', models.IntegerField(blank=True, null=True)),
                ('filled_slots', models.IntegerField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Organizations',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Gate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gates', to='organization.organization')),
            ],
            options={
                'verbose_name_plural': 'Gates',
                'managed': True,
            },
        ),
    ]
