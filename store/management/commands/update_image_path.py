from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    help = "Update image paths for products with default.jpg image"

    def handle(self, *args, **kwargs):
        products = Product.objects.filter(default_image__icontains="default.jpg")

        for product in products:

            if product.default_image:

                if "default.jpg" in product.default_image.name:

                    product.default_image = (
                        f"images/{product.default_image.name.split('/')[-1]}"
                    )
                    product.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully updated image paths for products with default.jpg image"
            )
        )
