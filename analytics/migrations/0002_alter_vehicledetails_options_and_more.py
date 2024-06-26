# Generated by Django 4.2.7 on 2024-02-17 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0007_vehicle_parking'),
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehicledetails',
            options={'ordering': ['-insurance_validity', '-puc_valid_type', '-id'], 'verbose_name_plural': 'Vehicle Details'},
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='currentAddress',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='fatherName',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='fuelType',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='insuranceName',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='insurancePolicyNo',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='manufacturerModel',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='ownerAddress',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='ownerMobileNo',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='ownerName',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='permanentAddress',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='permitNo',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='permitType',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='permitValidityFrom',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='permitValidityTo',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='pucValidUpto',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='registeredPlace',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='registrationDate',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='registrationNumber',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='seatingCapacity',
        ),
        migrations.RemoveField(
            model_name='vehicledetails',
            name='vehicleType',
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='fuel_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='insurance_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='insurance_validity',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='manufacturer_model',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='manufacturing_year',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='norms_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='owner_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='puc_valid_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='seating_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='vehicle_class',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehicledetails',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehicledetails',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_details', to='vehicle.vehicle'),
        ),
        migrations.DeleteModel(
            name='PerHourVehicleCount',
        ),
    ]
