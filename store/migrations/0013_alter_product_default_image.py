# Generated by Django 5.0.6 on 2024-07-09 19:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0012_product_default_image_alter_productphoto_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="default_image",
            field=models.ImageField(
                default="images/royce/default.jpg", upload_to="images/royce"
            ),
        ),
    ]
