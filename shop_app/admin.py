from django.contrib import admin

from .models import *


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    empty_value_display = 'Nothing'


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name",)
    empty_value_display = 'Nothing'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "spent_money",)
    empty_value_display = 'Nothing'
    list_select_related = ("cart", "wish_list")


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("nickname", "created_at_comment", "profile", "rating_products",)
    search_fields = ("nickname",)
    empty_value_display = 'Nothing'
    list_select_related = ("profile",)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "category", "price_for_what", "in_reality", 'created_at')
    search_fields = ('title',)
    empty_value_display = 'Nothing'
    list_select_related = ("category",)

class CheckoutAdmin(admin.ModelAdmin):
    readonly_fields = ('product_quality',)



admin.site.register(Category, CategoryAdmin)
admin.site.register(Compare)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(WishList)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Tag)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Coupon)
admin.site.register(DescriptionProductCart)
admin.site.register(Cart)
