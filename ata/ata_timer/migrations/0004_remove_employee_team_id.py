# Generated by Django 3.1.5 on 2021-01-16 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ata_timer', '0003_auto_20210116_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='team_id',
        ),
    ]
