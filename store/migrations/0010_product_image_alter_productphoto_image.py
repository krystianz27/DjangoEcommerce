# Generated by Django 5.0.6 on 2024-07-03 15:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0009_remove_product_image_productphoto"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(default="/images/default.jpg", upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="productphoto",
            name="image",
            field=models.ImageField(upload_to="images/"),
        ),
    ]
