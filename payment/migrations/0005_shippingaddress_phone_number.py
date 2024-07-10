# Generated by Django 5.0.6 on 2024-07-09 23:28

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0004_rename_address2_shippingaddress_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="shippingaddress",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None
            ),
        ),
    ]
