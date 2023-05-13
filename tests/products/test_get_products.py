import pytest
from django.shortcuts import get_object_or_404
from django.test import Client

from shop_app.models import Category, Product


@pytest.mark.django_db
def test_detail_product():
    client = Client()
    product = Product.objects.create(
        title="qwer",
        category=Category.objects.create(title="qwer_category"),
        price=123,
        price_for_what="ht",
        trademark="qwer",
        country="Ukraine",
        count_in_reality=3,
        photos="weqrqwerqwerwqr/qwerqwerqwer/",
    )
    response = client.get(
        f"/bsm_shop/{product.pk}/",
    )
    db_product = get_object_or_404(Product, pk=product.pk)
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_product():
    client = Client()
    product1 = Product.objects.create(
        title="qwer",
        category=Category.objects.create(title="qwer_category"),
        price=123,
        price_for_what="ht",
        trademark="qwer",
        country="Ukraine",
        count_in_reality=3,
        photos="weqrqwerqwerwqr/qwerqwerqwer/",
    )
    product2 = Product.objects.create(
        title="qwerqwer",
        category=Category.objects.create(title="qwer_category123"),
        price=1232,
        price_for_what="ht",
        trademark="qwer",
        country="Ukraine",
        count_in_reality=3,
        photos="weqrqwerqwerwqr/qwerqwerqwerqwer/",
    )
    response = client.get(
        f"/bsm_shop/",
    )
    db_product1 = get_object_or_404(Product, pk=product1.pk)
    db_product2 = get_object_or_404(Product, pk=product2.pk)
    assert response.status_code == 200
