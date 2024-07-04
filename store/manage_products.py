# Import Django modules
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.ecommerce.settings")
django.setup()

# Import necessary models
from store.models import Category, Product


def create_products_for_pants_category():
    # Check if category "pants" exists; if not, create it
    category, created = Category.objects.get_or_create(name="pants", slug="pants")

    # Create 15 example products assigned to category "pants"
    products = [
        {
            "title": f"Stylish Pants {i}",
            "brand": "FashionBrand",
            "description": f"Comfortable pants with stylish design {i}",
            "price": 49.99 + i * 5,  # Price increases with each product
            "category": category,  # Assign to "pants" category
        }
        for i in range(1, 16)  # Create 15 products
    ]

    # Create products in the database
    for product_data in products:
        Product.objects.create(**product_data)

    print("Created 15 products for category 'pants'.")


if __name__ == "__main__":
    create_products_for_pants_category()
