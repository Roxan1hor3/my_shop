from django import template
from django.utils.safestring import mark_safe

from shop_app.models import Category
from shop_app.special_variables import MAX_COUNT_STAR, FILLED_STARS, EMPTY_STARS

register = template.Library()


@register.filter(is_safe=True)
def create_star_rating(rating=MAX_COUNT_STAR):
    """ To output the rating in stars """
    html_star_rating = FILLED_STARS * rating
    html_star_rating += EMPTY_STARS * (MAX_COUNT_STAR - rating)
    return mark_safe(html_star_rating)


@register.filter()
def count(value=None):
    if value is None:
        value = []
    return len(value)


@register.simple_tag
def category_choice():
    """ To display categories in the headers """
    html_all_categories = '<option>All categories</option>\n'
    for item in Category.objects.all():
        html_all_categories += f"<option>{item.title}</option>\n"
    return mark_safe(html_all_categories)


@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)


@register.filter(name='discount_coupon')
def discount_coupon(total, discount):
    if discount is None:
        discount = 0
    return total * (100-discount) / 100


@register.filter(name='multiply')
def multiply(a, b):
    return a*b
