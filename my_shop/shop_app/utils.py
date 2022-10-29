from django.db.models import QuerySet


def get_sum_product(product: QuerySet, description: QuerySet, coupon: int = 0):
    sum_product = 0
    for product, desc in zip(product, description):
        sum_product += product.price * desc.quality
    sum_product = sum_product * (100 - coupon) / 100
    return sum_product
