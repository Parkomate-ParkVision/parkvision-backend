# Generated by Django 4.2.7 on 2024-02-12 16:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_remove_location_section_remove_section_floor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CCTV',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('parking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cctvs', to='parking.parking')),
            ],
        ),
    ]