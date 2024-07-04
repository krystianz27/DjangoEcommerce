# Generated by Django 5.0.6 on 2024-07-03 15:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0010_product_image_alter_productphoto_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="image",
        ),
        migrations.AlterField(
            model_name="productphoto",
            name="image",
            field=models.ImageField(default="/images/default.jpg", upload_to="images/"),
        ),
    ]