# Generated by Django 5.0.6 on 2024-06-25 19:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0006_alter_product_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(default="default.jpg", upload_to="images/"),
        ),
    ]