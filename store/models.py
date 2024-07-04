from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify

from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("list-category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="product", on_delete=models.CASCADE, null=True
    )

    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default="unbranded")
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from="title", unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    default_image = models.ImageField(
        default="/images/default.jpg", upload_to="images/"
    )

    def save(self, *args, **kwargs):
        if (
            not self.slug
            or self.title
            != Product.objects.filter(pk=self.pk)
            .values_list("title", flat=True)
            .first()
        ):
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse("product-info", args=[self.slug])


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        Product, related_name="photos", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="images/")
    is_main = models.BooleanField(default=False)
