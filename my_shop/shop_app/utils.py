from django.core.mail import send_mail
from django.db.models import QuerySet

from my_shop.settings import EMAIL_HOST_USER


def get_sum_product(product: QuerySet, description: QuerySet, coupon: int = 0):
    sum_product = 0
    for product, desc in zip(product, description):
        sum_product += product.price * desc.quality
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
