# Generated by Django 4.1.6 on 2023-03-07 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hall', '0002_remove_head_chip_ip_device_chip_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeadParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall.head')),
            ],
            options={
                'unique_together': {('key', 'head')},
            },
        ),
        migrations.CreateModel(
            name='DeviceParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall.device')),
            ],
            options={
                'unique_together': {('key', 'device')},
            },
        ),
    ]
