import pytest
from django.shortcuts import get_object_or_404
from django.test import Client

from shop_app.models import Category, Comments, Product


@pytest.mark.django_db
def test_add_comment():
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
    response = client.post(
        f"/bsm_shop/comments/{product.pk}/",
        data=dict(
            rating_products="5",
            nickname="1234",
            email="Roxanasfdqwefhor@gmail.com",
            description_comment="1234",
        ),
    )
    comment = get_object_or_404(Comments, pk=1)
    product = get_object_or_404(Product, pk=product.pk)
    assert comment.email == "Roxanasfdqwefhor@gmail.com"
    assert comment.description_comment == "1234"
    assert comment.rating_products == 5
    assert product.count_comments == 1
