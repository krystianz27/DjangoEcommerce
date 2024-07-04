import pytest
from store.models import Category, Product


@pytest.mark.django_db
def test_product_str():
    category = Category(name="Electronics", slug="electronics")
    product = Product(
        category=category,
        title="Laptop",
        brand="Lenovo",
        description="A powerful laptop",
        price=999.99,
        image="media/images/default.jpg",
    )
    assert str(product) == "Laptop"
