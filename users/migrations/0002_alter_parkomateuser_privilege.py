# Generated by Django 4.2.7 on 2024-02-12 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkomateuser',
            name='privilege',
            field=models.IntegerField(choices=[(0, 'SUPERUSER'), (1, 'ADMIN')], default=0),
        ),
    ]
