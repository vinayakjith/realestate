# Generated by Django 5.0.6 on 2025-01-14 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0013_alter_property_google'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='has_paid',
        ),
    ]
