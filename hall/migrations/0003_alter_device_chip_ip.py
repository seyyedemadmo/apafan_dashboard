# Generated by Django 4.1.6 on 2023-03-05 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hall', '0002_remove_head_chip_ip_device_chip_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='chip_ip',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
