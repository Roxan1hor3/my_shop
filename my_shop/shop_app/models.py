from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Product(models.Model):
    title = models.CharField(max_length=150)
    big_description_product = models.TextField(max_length=500, blank=True)
    small_description_product = models.TextField(max_length=500, blank=True)
    price = models.FloatField()
    price_for_what = models.CharField(max_length=20)
    in_reality = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photos = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, default='Others')
    trademark = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    count_in_reality = models.IntegerField(blank=True)
    discount = models.IntegerField(blank=True, default=0)
    tags = models.ManyToManyField('Tag', blank=True)
    avg_rating = models.IntegerField(blank=True, default=5)
    count_comments = models.IntegerField(blank=True, default=0)

    def total(self):
        if self.discount == 0:
            self.discount = 100
        return self.price * self.discount / 100

    def get_absolute_url(self):
        return f'/bsm_shop/{self.pk}/'

    def __str__(self):
        return f'{self.title}, {self.category}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['title']


class Coupon(models.Model):
    title = models.CharField(max_length=150)
    discount = models.IntegerField(blank=True, default=0)
    is_active = models.BooleanField(default=False)


class Category(models.Model):
    title = models.CharField(max_length=150, )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Сategories'
        ordering = ['title']


class Comments(models.Model):
    nickname = models.CharField(max_length=150, validators=[MinLengthValidator(4)])
    description_comment = models.TextField(max_length=500)
    created_at_comment = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    rating_products = models.IntegerField(default=5)
    email = models.EmailField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/bsm_shop/{self.pk}/'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['profile']


class Profile(User):
    count_of_buy = models.IntegerField(default=0)
    phone = PhoneNumberField()
    spent_money = models.FloatField(blank=True, default=0)
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE)
    wish_list = models.OneToOneField('WishList', on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    history_of_buy = models.ManyToManyField('Product', blank=True)
    coupon = models.ForeignKey('Coupon', blank=True, null=True, on_delete=models.SET_NULL)
    coupon_history = models.CharField(max_length=300, blank=True)
    count_product_in_wish_list = models.IntegerField(default=0, blank=True)
    count_product_in_cart = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f'{super().username}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Cart(models.Model):
    products_in_the_cart = models.ManyToManyField('Product', blank=True, through='DescriptionProductCart')


class DescriptionProductCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quality = models.PositiveIntegerField(default=1, blank=True)


class WishList(models.Model):
    products_in_the_preferences = models.ManyToManyField('Product', blank=True)


class Checkout(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    postcode = models.CharField(max_length=150)
    product_to_buy = models.ManyToManyField('Product', blank=True)
    price = models.FloatField(default=0, blank=True)


class Compare(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
    product_to_compare = models.ManyToManyField('Product', blank=True)


class ContactUs(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    your_message = models.TextField(max_length=300)


class Tag(models.Model):
    title = models.CharField(max_length=150, )
