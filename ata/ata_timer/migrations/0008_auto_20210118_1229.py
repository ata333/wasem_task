# Generated by Django 3.1.5 on 2021-01-18 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ata_timer', '0007_employee_team_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='check_in_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='check in time'),
        ),
    ]
