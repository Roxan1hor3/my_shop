from random import randint

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import redirect, get_object_or_404, render, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, FormView, UpdateView
from django.views.generic.base import View

from my_shop.settings import EMAIL_HOST_USER
from shop_app.forms import CommentsForm, UserRegisterForm, CheckoutForm
from shop_app.models import Product, Profile, WishList, Cart, DescriptionProductCart, Coupon, Checkout

'''Доробить купон для none, лайки, проще ссилки'''


class CreateCommentsView(View):
    @staticmethod
    def post(request, pk):
        """ Save a new comment """
        form = CommentsForm(request.POST)
        product = get_object_or_404(Product, pk=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()
        """ Update the number of comments """
        product.count_comments = get_object_or_404(Product, pk=pk).comments_set.all().count()
        """ Update the avg_rating """
        try:
            product.avg_rating = round(
                get_object_or_404(Product, pk=pk).comments_set.all().aggregate(Avg('rating_products'))[
                    "rating_products__avg"])
        except TypeError:
            product.avg_rating = 5
        product.save()
        return redirect(f"/bsm_shop/{pk}/")


class ProductDetailView(DetailView):
    """ Information about one product """
    model = Product
    template_name = 'shop_app/product-details.html'

    def get_queryset(self):
        """ Take category and tags """
        return super().get_queryset().filter(pk=self.kwargs["pk"]).select_related(
            'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """ Take comments """
        context['comments'] = get_object_or_404(super().get_queryset(), pk=self.kwargs["pk"]).comments_set.all()
        if self.request.user.is_authenticated:
            context["profile"] = self.request.user.profile
        return context


class ProductListView(ListView):
    """ All products """
    paginate_by = 4
    model = Product
    template_name = 'shop_app/shop.html'

    def get_queryset(self):
        return super().get_queryset().select_related('category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        """ For hearts that add or remove products from the wishlist """
        if self.request.user.is_authenticated:
            context['profile'] = self.request.user.profile
            """ Cart window navbar """
            context['cart'] = Cart.objects.filter(pk=context['profile'].cart_id).prefetch_related(
                'products_in_the_cart').get()
            context['wish_list'] = WishList.objects.filter(pk=context['profile'].wish_list_id).prefetch_related(
                'products_in_the_preferences').get()
            context['description'] = get_list_or_404(DescriptionProductCart, cart_id=context['profile'].cart_id)
            sum_product = 0
            for product, desc in zip(context['cart'].products_in_the_cart.all(), context['description']):
                sum_product += product.price * desc.quality
            context['sum_product'] = sum_product
        return context


class AccountRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'shop_app/register.html'

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        form = form.save(commit=False)
        username = form.username
        """ Active account """
        form.is_active = False
        """ Create wishlist """
        form.wish_list = WishList.objects.create()
        """ Create cart """
        form.cart = Cart.objects.create()
        form.save()
        profile = get_object_or_404(Profile, username=username)
        """ Send mail """
        send_mail(subject='Bsm_shop account confirmation',
                  message=f'Hello {profile.username} click on the button to confirm the account\n '
                          f'127.0.0.1:8000/bsm_shop/my-account/confirm/{profile.pk}',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[form.email],
                  fail_silently=False,
                  )
        return super().form_valid(form)


class AccountLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'shop_app/login.html'

    def get_success_url(self):
        return reverse_lazy('bsm-shop')


class AccountLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('bsm-shop')


class AccountUpdateView(UpdateView):
    model = Profile
    fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    template_name = 'shop_app/my-account.html'

    def get_success_url(self):
        return reverse_lazy('my-account', args=[self.kwargs["pk"]])


class ActivateAccountView(View):
    """ Activate the account and redirect to 'login' """

    @staticmethod
    def get(request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        profile.is_active = True
        profile.save()
        return redirect(f"/bsm_shop/login")


class WishlistView(DetailView):
    model = WishList
    template_name = 'shop_app/wishlist.html'

    def get_queryset(self, **kwargs):
        """ Take products from wishlist """
        return super().get_queryset().filter(pk=self.kwargs['pk']).prefetch_related(
            'products_in_the_preferences')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = self.request.user.profile
        return context


class AddProductToWishList(View):
    @staticmethod
    def get(request, product_id, wish_list_id):
        wishlist = get_object_or_404(WishList, pk=wish_list_id)
        wishlist.products_in_the_preferences.add(get_object_or_404(Product, pk=product_id))
        wishlist.save()
        profile = request.user.profile
        profile.count_product_in_wish_list += 1
        profile.save()
        return redirect(request.META.get('HTTP_REFERER'))


class RemoveProductFromWishList(View):
    @staticmethod
    def get(request, product_id, wish_list_id):
        wishlist = get_object_or_404(WishList, pk=wish_list_id)
        wishlist.products_in_the_preferences.remove(get_object_or_404(Product, pk=product_id))
        wishlist.save()
        profile = request.user.profile
        profile.count_product_in_wish_list -= 1
        profile.save()
        return redirect(request.META.get('HTTP_REFERER'))


class CartView(DetailView):
    model = Cart
    template_name = 'shop_app/cart.html'

    def get_queryset(self, **kwargs):
        """ Take products from cart """
        return super().get_queryset().filter(pk=self.kwargs['pk']).prefetch_related('products_in_the_cart')

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data()
        context['profile'] = self.request.user.profile
        context['description'] = get_list_or_404(DescriptionProductCart, cart_id=self.kwargs['pk'])
        sum_product = 0
        for product, desc in zip(self.object.products_in_the_cart.all(), context['description']):
            sum_product += product.price * desc.quality
        context['sum_product'] = sum_product
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
        return redirect(request.META.get('HTTP_REFERER'))


class RemoveProductFromCart(View):
    @staticmethod
    def get(request, product_id, cart_id):
        cart = get_object_or_404(Cart, pk=cart_id)
        cart.products_in_the_cart.remove(get_object_or_404(Product, pk=product_id))
        cart.save()
        profile = request.user.profile
        profile.count_product_in_cart -= 1
        profile.save()
        return redirect(request.META.get('HTTP_REFERER'))


class ChangeQuality(View):
    @staticmethod
    def post(request, cart_id):
        request_dict = request.POST.dict()
        dpc = DescriptionProductCart.objects.filter(cart_id=cart_id)
        for tuplekv, dpc in tuple(zip(list(request_dict.items())[1:-1], dpc)):
            dpc.quality = tuplekv[1]
            dpc.save()
        return redirect(request.META.get('HTTP_REFERER'))


class SetCoupon(View):
    @staticmethod
    def post(request, profile_id):
        request_dict = request.POST.dict()
        profile = get_object_or_404(Profile, pk=profile_id)
        coupon = get_object_or_404(Coupon, title=request_dict['coupon'])
        profile.coupon = coupon
        profile.save()
        return redirect(request.META.get('HTTP_REFERER'))


class CheckoutView(View):
    @staticmethod
    def post(request, profile_id, cart_id):
        form = CheckoutForm(request.POST)
        profile = get_object_or_404(Profile, pk=profile_id)
        cart = Cart.objects.filter(pk=cart_id).prefetch_related('products_in_the_cart').get()
        description = get_list_or_404(DescriptionProductCart, cart_id=cart_id)
        sum_product = 0
        for product, desc in zip(cart.products_in_the_cart.all(), description):
            sum_product += product.price * desc.quality
        if form.is_valid():
            form = form.save(commit=False)
            form.profile = profile
            form.price = sum_product
            send_mail(subject=f'Checkout {form.profile.username}',
                      message=f'Hello {form.profile.username} you buy \n '
                              f'price {form.price}',
                      from_email=EMAIL_HOST_USER,
                      recipient_list=[form.profile.email],
                      fail_silently=False,
                      )
            form.save()
            checkout = Checkout.objects.last()
            checkout.product_to_buy.add(cart.products_in_the_cart.all())
            checkout.save()
        else:
            send_mail(subject=f'Checkout {profile.username}',
                      message=f'Error',
                      from_email=EMAIL_HOST_USER,
                      recipient_list=[profile.email],
                      fail_silently=False,
                      )
        return redirect(f'/bsm_shop/cart/{cart_id}')

    @staticmethod
    def get(request, profile_id, cart_id):
        cart = Cart.objects.filter(pk=cart_id).prefetch_related('products_in_the_cart').get()
        profile = get_object_or_404(Profile, pk=profile_id)
        description = get_list_or_404(DescriptionProductCart, cart_id=cart_id)
        sum_product = 0
        for product, desc in zip(cart.products_in_the_cart.all(), description):
            sum_product += product.price * desc.quality
        return render(request, 'shop_app/checkout.html', context={
            'cart': cart,
            'profile': profile,
            'description': description,
            'sum_product': sum_product,
        })
