# Generated by Django 3.1.5 on 2021-01-16 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ata_timer', '0005_employee_team_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='team_id',
        ),
    ]