from django.urls import path

from .views import *

urlpatterns = [
    path("filter", FilterProductView.as_view(), name="filter-product"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("", ProductListView.as_view(), name="bsm-shop"),
    path("comments/<int:pk>/", CreateCommentsView.as_view(), name="create-comments"),
    path("my-account/<int:pk>/", AccountUpdateView.as_view(), name="my-account"),
    path("my-account/register/", AccountRegisterView.as_view(), name="register"),
    path("my-account/confirm/<int:pk>/", ActivateAccountView.as_view(), name="confirm"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("login/", AccountLoginView.as_view(), name="login"),
    path("wishlist/<int:pk>/", WishlistView.as_view(), name="wishlist"),
    path(
        "wishlist_append/<int:product_id>/<int:wish_list_id>",
        AddProductToWishList.as_view(),
        name="wishlist_append",
    ),
    path(
        "wishlist_remove/<int:product_id>/<int:wish_list_id>",
        RemoveProductFromWishList.as_view(),
        name="wishlist_remove",
    ),
    path("cart/<int:pk>/", CartView.as_view(), name="cart"),
    path(
        "cart_append/<int:product_id>/<int:cart_id>",
        AddProductToCart.as_view(),
        name="cart_append",
    ),
    path(
        "cart_remove/<int:product_id>/<int:cart_id>",
        RemoveProductFromCart.as_view(),
        name="cart_remove",
    ),
    path(
        "cart/quality_cart/<int:cart_id>", ChangeQuality.as_view(), name="quality_cart"
    ),
    path("cart/set_coupon/<int:profile_id>", SetCoupon.as_view(), name="set_coupon"),
    path(
        "checkout/<int:profile_id>/<int:cart_id>",
        CheckoutView.as_view(),
        name="checkout",
    ),
]
