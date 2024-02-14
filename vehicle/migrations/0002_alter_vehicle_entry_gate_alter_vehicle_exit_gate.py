# Generated by Django 4.2.7 on 2024-02-14 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_alter_organization_admins'),
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='entry_gate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entry_vehicle', to='organization.gate'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='exit_gate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exit_vehicke', to='organization.gate'),
        ),
    ]
