# Generated by Django 4.2.7 on 2024-02-16 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0003_alter_vehicle_exit_gate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ['-entry_time'], 'verbose_name': 'Vehicle', 'verbose_name_plural': 'Vehicles'},
        ),
        migrations.AlterModelTable(
            name='vehicle',
            table='vehicle',
        ),
    ]
