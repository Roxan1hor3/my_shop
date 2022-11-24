from django.core.mail import send_mail
from django.db.models import QuerySet, Q

from my_shop.settings import EMAIL_HOST_USER
from shop_app.models import Product


def get_sum_product(product: QuerySet, description: QuerySet, coupon: int):
    sum_product = 0
    if coupon is None:
        coupon = 0
    for product, description in zip(product, description):
        sum_product += product.price * description.quality
    sum_product = sum_product * (100 - coupon) / 100
    return sum_product


def create_product_quality(product: QuerySet, description: QuerySet):
    document = ''
    for product, desc in zip(product, description):
        document += f'{product.title}- quality - {desc.quality}\n'
    return document


def send_email_checkout(checkout, profile):
    send_mail(subject=f'Checkout {checkout.profile.username}',
              message=f'Hello {checkout.profile.username} you buy \n '
                      f'price {checkout.price}',
              from_email=EMAIL_HOST_USER,
              recipient_list=[profile.email],
              fail_silently=False,
              )


def send_email_error(profile):
    send_mail(subject=f'Checkout {profile.username}',
              message=f'Error',
              from_email=EMAIL_HOST_USER,
              recipient_list=[profile.email],
              fail_silently=False,
              )


def filter_func(category_pk, price__gte, price__lte, star, tags):
    queryset = Product.objects.filter(Q(price__gte=price__gte) & Q(price__lte=price__lte)).select_related(
        'category').prefetch_related('tags')
    if category_pk:
        queryset = queryset.filter(category__in=category_pk).distinct()
    if star:
        queryset = queryset.filter(avg_rating__in=star).distinct()
    if tags:
        queryset = queryset.filter(tags__in=tags).distinct()
    return queryset
