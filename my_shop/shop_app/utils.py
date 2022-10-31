from django.db.models import QuerySet


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
