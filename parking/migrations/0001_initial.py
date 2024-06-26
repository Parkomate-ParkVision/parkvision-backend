# Generated by Django 4.2.7 on 2024-02-12 10:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('number', models.IntegerField(auto_created=True, default=1, primary_key=True, serialize=False, unique=True)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('name', models.CharField(auto_created=True, default='A', max_length=100, primary_key=True, serialize=False, unique=True)),
                ('isActive', models.BooleanField(default=True)),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='parking.floor')),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('floorsCount', models.IntegerField(default=0)),
                ('sectionsCount', models.IntegerField(default=0)),
                ('locationsCount', models.IntegerField(default=0)),
                ('isActive', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parkings', to='organization.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('isOccupied', models.BooleanField(default=False)),
                ('isAllocated', models.BooleanField(default=False)),
                ('isActive', models.BooleanField(default=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='parking.section')),
            ],
        ),
        migrations.AddField(
            model_name='floor',
            name='parking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floors', to='parking.parking'),
        ),
    ]
