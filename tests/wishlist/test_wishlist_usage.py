import pytest
from django.shortcuts import get_object_or_404
from django.test import Client

from shop_app.models import Cart, Category, Product, Profile, WishList


@pytest.mark.django_db
def test_get_wish_list():
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
    profile = Profile.objects.create_user(
        username="Roxan1hor333",
        first_name="Roxan1hor3334312",
        last_name="Roxan1hor3334123421",
        password="!234QWERasdf",
        email="Roxanhor@gmail.com",
        phone="+380988181628",
        is_active=True,
        cart=Cart.objects.create(),
        wish_list=WishList.objects.create(),
    )
    profile.wish_list.products_in_the_preferences.add(product1)
    profile.wish_list.products_in_the_preferences.add(product2)
    profile.save()
    client.force_login(user=profile)
    response = client.get(
        f"/bsm_shop/wishlist/{profile.pk}/",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_append_remove_product_from_wish_list():
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
    wish_list = WishList.objects.create()
    profile = Profile.objects.create_user(
        username="Roxan1hor333",
        first_name="Roxan1hor3334312",
        last_name="Roxan1hor3334123421",
        password="!234QWERasdf",
        email="Roxanhor@gmail.com",
        phone="+380988181628",
        is_active=True,
        wish_list=wish_list,
        cart=Cart.objects.create(),
    )
    client.force_login(user=profile)
    response = client.get(
        f"/bsm_shop/wishlist_append/{product.pk}/{wish_list.pk}",
    )
    assert response.status_code == 302
    profile = get_object_or_404(Profile, pk=profile.pk)
    assert profile.wish_list.products_in_the_preferences.count() == 1
    response = client.get(
        f"/bsm_shop/wishlist_remove/{product.pk}/{wish_list.pk}",
    )
    profile = get_object_or_404(Profile, pk=profile.pk)
    assert profile.wish_list.products_in_the_preferences.count() == 0
