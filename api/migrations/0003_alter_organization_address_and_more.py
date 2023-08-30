# Generated by Django 4.2 on 2023-08-30 19:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_gate_alter_organization_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="entry_gates",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="exit_gates",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="filled_slots",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="total_slots",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="cropped_image",
            field=models.URLField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="number_plate",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="prediction",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="vehicle_image",
            field=models.URLField(blank=True, null=True, unique=True),
        ),
    ]
