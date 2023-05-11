import factory

from shop_app.models import Cart, Coupon, Profile, WishList


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    # profile = factory.SubFactory(ProfileFactory)


class WishListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishList

    profile = factory.SubFactory(ProfileFactory)


class CouponFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Coupon

    profile = factory.SubFactory(ProfileFactory)
