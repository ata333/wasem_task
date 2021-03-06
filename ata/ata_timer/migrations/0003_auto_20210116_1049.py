# Generated by Django 3.1.5 on 2021-01-16 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ata_timer', '0002_auto_20210115_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='team_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ata_timer.team'),
            preserve_default=False,
        ),
    ]
