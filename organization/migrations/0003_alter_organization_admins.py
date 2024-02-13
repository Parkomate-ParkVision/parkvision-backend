# Generated by Django 4.2.7 on 2024-02-13 16:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_organization_admins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='admins',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), blank=True, null=True, size=None),
        ),
    ]
