from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import redirect, get_object_or_404, render, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView, ListView
from django.views.generic.base import View

from my_shop.settings import EMAIL_HOST_USER
from shop_app.forms import CommentsForm, UserRegisterForm, CheckoutForm
from shop_app.models import (
    Product,
    Profile,
    WishList,
    Cart,
    DescriptionProductCart,
    Coupon,
    Checkout,
    Category,
    Tag,
)
from shop_app.utils import (
    get_sum_product,
    create_product_quality,
    send_email_checkout,
    send_email_error,
    filter_func,
)


class CreateCommentsView(View):
    @staticmethod
    def post(request, pk):
        """Save a new comment"""
        form = CommentsForm(request.POST)
        product = get_object_or_404(Product, pk=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()
        """ Update the number of comments """
        product.count_comments = (
            get_object_or_404(Product, pk=pk).comments_set.all().count()
        )
        """ Update the avg_rating """
        try:
            product.avg_rating = round(
                get_object_or_404(Product, pk=pk)
                .comments_set.all()
                .aggregate(Avg("rating_products"))["rating_products__avg"]
            )
        except TypeError:
            product.avg_rating = 5
        product.save()
        return redirect(f"/bsm_shop/{pk}/")


class ProductDetailView(DetailView):
    """Information about one product"""

    model = Product
    template_name = "shop_app/product-details.html"

    def get_queryset(self):
        """Take category and tags"""
        return (
            super()
            .get_queryset()
            .filter(pk=self.kwargs["pk"])
            .select_related("category")
            .prefetch_related("tags")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """ Take comments """
        context["comments"] = get_object_or_404(
            super().get_queryset(), pk=self.kwargs["pk"]
        ).comments_set.all()
        if self.request.user.is_authenticated:
            context["profile"] = self.request.user.profile
        return context


class ProductListView(ListView):
    """All products"""

    paginate_by = 4
    model = Product
    template_name = "shop_app/shop.html"

    def get_queryset(self):
        return (
            super().get_queryset().select_related("category").prefetch_related("tags")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        """ For hearts that add or remove products from the wishlist """
        context["categores"] = Category.objects.all()
        if self.request.user.is_authenticated:
            context["profile"] = self.request.user.profile
            """ Cart window navbar """
            context["cart"] = (
                Cart.objects.filter(profile=context["profile"])
                .prefetch_related("products_in_the_cart")
                .get()
            )
            context["wish_list"] = (
                WishList.objects.filter(profile=context["profile"])
                .prefetch_related("products_in_the_preferences")
                .get()
            )
            context["checkouts"] = Checkout.objects.filter(
                profile=context["profile"]
            ).prefetch_related("product_to_buy")
            context["tags"] = Tag.objects.all()
            if context["cart"].products_in_the_cart.all():
                context["description"] = get_list_or_404(
                    DescriptionProductCart, cart_id=context["profile"].cart_id
                )
                context["sum_product"] = get_sum_product(
                    context["cart"].products_in_the_cart.all(), context["description"]
                )
        return context


class FilterProductView(ProductListView):
    def get_queryset(self):
        category_pk = self.request.GET.getlist("category")
        price__gte = self.request.GET.get("price__gte")
        price__lte = self.request.GET.get("price__lte")
        star = self.request.GET.getlist("star")
        tags = self.request.GET.getlist("tags")
        try:
            queryset = filter_func(category_pk, price__gte, price__lte, star, tags)
        except ValueError:
            price__gte = 0
            price__lte = 99999999
            queryset = filter_func(category_pk, price__gte, price__lte, star, tags)

        return queryset


class AccountRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "shop_app/register.html"

    def get_success_url(self):
        return reverse_lazy("login")

    def form_valid(self, form):
        form = form.save(commit=False)
        username = form.username
        """ Active account """
        form.is_active = False
        """ Create wishlist """
        form.wish_list = WishList.objects.create()
        """ Create cart """
        form.cart = Cart.objects.create()
        DescriptionProductCart.objects.create(cart=form.cart)
        form.save()
        profile = get_object_or_404(Profile, username=username)
        """ Send mail """
        send_mail(
            subject="Bsm_shop account confirmation",
            message=f"Hello {profile.username} click on the button to confirm the account\n "
            f"127.0.0.1:8000/bsm_shop/my-account/confirm/{profile.pk}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[form.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class AccountLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "shop_app/login.html"

    def get_success_url(self):
        return reverse_lazy("bsm-shop")


class AccountLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy("bsm-shop")


class AccountUpdateView(UpdateView):
    model = Profile
    fields = ["username", "email", "phone", "first_name", "last_name"]
    template_name = "shop_app/my-account.html"

    def get_success_url(self):
        return reverse_lazy("my-account", args=[self.kwargs["pk"]])


class ActivateAccountView(View):
    @staticmethod
    def get(request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        profile.is_active = True
        profile.save()
        return redirect(f"/bsm_shop/login")


class WishlistView(DetailView):
    model = WishList
    template_name = "shop_app/wishlist.html"

    def get_queryset(self, **kwargs):
        """Take products from wishlist"""
        return (
            super()
            .get_queryset()
            .filter(pk=self.kwargs["pk"])
            .prefetch_related("products_in_the_preferences")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["profile"] = self.request.user.profile
        return context


class AddProductToWishList(View):
    @staticmethod
    def get(request, product_id, wish_list_id):
        wishlist = get_object_or_404(WishList, pk=wish_list_id)
        wishlist.products_in_the_preferences.add(
            get_object_or_404(Product, pk=product_id)
        )
        wishlist.save()
        profile = request.user.profile
        profile.count_product_in_wish_list += 1
        profile.save()
        return redirect(request.META.get("HTTP_REFERER"))


class RemoveProductFromWishList(View):
    @staticmethod
    def get(request, product_id, wish_list_id):
        wishlist = get_object_or_404(WishList, pk=wish_list_id)
        wishlist.products_in_the_preferences.remove(
            get_object_or_404(Product, pk=product_id)
        )
        wishlist.save()
        profile = request.user.profile
        profile.count_product_in_wish_list -= 1
        profile.save()
        return redirect(request.META.get("HTTP_REFERER"))


class CartView(DetailView):
    model = Cart
    template_name = "shop_app/cart.html"

    def get_queryset(self, **kwargs):
        """Take products from cart"""
        return (
            super()
            .get_queryset()
            .filter(pk=self.kwargs["pk"])
            .prefetch_related("products_in_the_cart")
        )

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data()
        context["profile"] = self.request.user.profile
        if self.get_queryset().get().products_in_the_cart.all():
            context["description"] = get_list_or_404(
                DescriptionProductCart, cart_id=self.kwargs["pk"]
            )
            context["sum_product"] = get_sum_product(
                self.object.products_in_the_cart.all(), context["description"]
            )
        return context


class AddProductToCart(View):
    @staticmethod
    def get(request, product_id, cart_id):
        cart = get_object_or_404(Cart, pk=cart_id)
        cart.products_in_the_cart.add(get_object_or_404(Product, pk=product_id))
        cart.save()
        profile = request.user.profile
        profile.count_product_in_cart += 1
        profile.save()
        return redirect(request.META.get("HTTP_REFERER"))


class RemoveProductFromCart(View):
    @staticmethod
    def get(request, product_id, cart_id):
        cart = get_object_or_404(Cart, pk=cart_id)
        cart.products_in_the_cart.remove(get_object_or_404(Product, pk=product_id))
        cart.save()
        profile = request.user.profile
        profile.count_product_in_cart -= 1
        profile.save()
        return redirect(request.META.get("HTTP_REFERER"))


class ChangeQuality(View):
    @staticmethod
    def post(request, cart_id):
        request_dict = request.POST.dict()
        dpc = Cart.objects.filter(pk=cart_id).get().product_description.all()
        """ request_dict.values())[1:-1] => take quality from request_dict """
        for quality, dpc in zip(list(request_dict.values())[1:-1], dpc):
            dpc.quality = quality
            dpc.save()
        return redirect(request.META.get("HTTP_REFERER"))


class SetCoupon(View):
    @staticmethod
    def post(request, profile_id):
        request_dict = request.POST.dict()
        profile = get_object_or_404(Profile, pk=profile_id)
        coupon = get_object_or_404(Coupon, title=request_dict["coupon"])
        profile.coupon = coupon
        profile.save()
        return redirect(request.META.get("HTTP_REFERER"))


class CheckoutView(View):
    @staticmethod
    def post(request, profile_id, cart_id):
        """Place order"""
        form = CheckoutForm(request.POST)
        profile = get_object_or_404(Profile, pk=profile_id)
        cart = (
            Cart.objects.filter(pk=cart_id)
            .prefetch_related("products_in_the_cart")
            .get()
        )
        description = get_list_or_404(DescriptionProductCart, cart_id=cart_id)

        sum_product = get_sum_product(
            cart.products_in_the_cart.all(), description, profile.coupon.discount
        )

        if form.is_valid():
            form = form.save(commit=False)
            form.profile = profile
            form.price = sum_product
            form.save()
            """ add product to checkout """
            checkout = Checkout.objects.last()
            checkout.product_quality = create_product_quality(
                cart.products_in_the_cart.all(), description
            )
            checkout.product_to_buy.add(*cart.products_in_the_cart.all())
            send_email_checkout(checkout, profile)
            checkout.save()
            """ clear counts of product for navbar """
            cart.products_in_the_cart.clear()
            wish_list = (
                WishList.objects.filter(pk=profile.wish_list_id)
                .prefetch_related("products_in_the_preferences")
                .get()
            )
            wish_list.products_in_the_preferences.clear()
            profile.count_product_in_wish_list = 0
            profile.count_product_in_cart = 0
            profile.save()
        else:
            send_email_error(profile)
        return redirect(f"/bsm_shop/cart/{cart_id}")

    @staticmethod
    def get(request, profile_id, cart_id):
        cart = (
            Cart.objects.filter(pk=cart_id)
            .prefetch_related("products_in_the_cart")
            .get()
        )
        profile = get_object_or_404(Profile, pk=profile_id)
        description = get_list_or_404(DescriptionProductCart, cart_id=cart_id)
        sum_product = get_sum_product(cart.products_in_the_cart.all(), description)
        return render(
            request,
            "shop_app/checkout.html",
            context={
                "cart": cart,
                "profile": profile,
                "description": description,
                "sum_product": sum_product,
            },
        )
