# Generated by Django 5.0.6 on 2025-01-11 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0011_remove_payment_payment_intent_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='google',
            field=models.CharField(default='', max_length=250),
        ),
    ]