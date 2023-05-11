import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from shop_app.models import Profile


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
    profile = Profile.objects.get(username="Roxan1hor333")
    assert profile.username == "Roxan1hor333"
