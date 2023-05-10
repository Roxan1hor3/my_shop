from django.shortcuts import get_object_or_404
from django.test import Client

from shop_app.models import Profile, Cart, WishList
from tests.factories import ProfileFactory, WishListFactory

from tests.users.endpoints import LOGIN
import pytest


@pytest.mark.django_db
def test_register():
    client = Client()
    response = client.post(
        "/bsm_shop/my-account/register/",
        data=dict(
            username="QWqwerasdf",
            first_name="WQEFRQW",
            last_name="QWERQWQQ",
            email="Roxan1hor333@gmail.com",
            phone="+380988181628",
            password1="1234QWERasdf",
            password2="1234QWERasdf",
        ),
    )
    print(response)
    # assert response.status_code == 403
    # profile = Profile.objects.create(
    #     cart=Cart.objects.create(),
    #     wish_list=WishList.objects.create(),
    #     username="Roxan",
    #     password="qwerasdf123",
    # )
    # profile.save()
    profile = Profile.objects.all()
    print(profile)
    # response = client.post(LOGIN, data=dict(username="Roxan", password="qwerasdf123"))
    # assert response.status_code == 200
