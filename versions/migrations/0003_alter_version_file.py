# Generated by Django 4.1.6 on 2023-05-06 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('versions', '0002_alter_version_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='file',
            field=models.FilePathField(path='data/version/'),
        ),
    ]
