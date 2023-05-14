import pytest
from django.shortcuts import get_object_or_404
from django.test import Client

from shop_app.models import Cart, Coupon, Profile, WishList


@pytest.mark.django_db
def test_set_coupon():
    client = Client()
    profile = Profile.objects.create(
        username="Roxan1hor333",
        first_name="Roxan1hor3334312",
        last_name="Roxan1hor3334123421",
        email="Roxanhor@gmail.com",
        phone="+380988181628",
        password="!234QWERasdf",
        is_active=True,
        cart=Cart.objects.create(),
        wish_list=WishList.objects.create(),
    )
    coupon = Coupon.objects.create(title="qwer", discount=12, is_active=True)
    response = client.post(
        f"/bsm_shop/cart/set_coupon/{profile.pk}",
        data=dict(coupon="qwer", apply_coupon=""),
    )
    assert response.status_code == 302
    db_profile = get_object_or_404(Profile, pk=profile.pk)
    db_coupon = get_object_or_404(Coupon, title=coupon.title)
    assert db_profile.coupon == db_coupon
    assert db_profile.is_active is True
