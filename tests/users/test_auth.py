import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from shop_app.models import Cart, Profile, WishList


@pytest.mark.django_db
def test_register():
    client = Client()
    response = client.post(
        "/bsm_shop/my-account/register/",
        data=dict(
            username="Roxan1hor333",
            first_name="Roxan1hor3334312",
            last_name="Roxan1hor3334123421",
            email="Roxanhor@gmail.com",
            phone="+380988181628",
            password1="!234QWERasdf",
            password2="!234QWERasdf",
        ),
    )
    assertRedirects(response, reverse("login"))
    db_profile = Profile.objects.get(username="Roxan1hor333")
    assert db_profile.username == "Roxan1hor333"


@pytest.mark.django_db
def test_activate_account():
    client = Client()
    profile = Profile.objects.create(
        username="Roxan1hor333",
        first_name="Roxan1hor3334312",
        last_name="Roxan1hor3334123421",
        email="Roxanhor@gmail.com",
        phone="+380988181628",
        password="!234QWERasdf",
        is_active=False,
        cart=Cart.objects.create(),
        wish_list=WishList.objects.create(),
    )
    response = client.get(
        f"/bsm_shop/my-account/confirm/{profile.pk}/",
    )
    db_profile = Profile.objects.get(username="Roxan1hor333")
    assert db_profile.username == "Roxan1hor333"
    assert db_profile.is_active is True


@pytest.mark.django_db
def test_update_account():
    client = Client()
    profile = Profile.objects.create(
        username="Roxan1hor333",
        first_name="Roxan1hor3334312",
        last_name="Roxan1hor3334123421",
        email="Roxanhor@gmail.com",
        phone="+380988181628",
        password="!234QWERasdf",
        is_active=False,
        cart=Cart.objects.create(),
        wish_list=WishList.objects.create(),
    )
    response = client.post(
        f"/bsm_shop/my-account/{profile.pk}/",
        data=dict(
            username="qwerqwer",
            first_name="Roxan1hor3334312",
            last_name="Roxan1hor3334123421",
            email="Roxanhor@gmail.com",
            phone="+380988181628",
        ),
    )
    db_profile = Profile.objects.get(pk=profile.pk)
    assert db_profile.username == "qwerqwer"
