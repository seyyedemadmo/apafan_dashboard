# Generated by Django 4.1.6 on 2023-02-14 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hall', '0002_remove_company_admin_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Group',
            new_name='Squad',
        ),
    ]
