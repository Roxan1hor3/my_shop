# Generated by Django 4.1.1 on 2022-11-19 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop_app", "0027_alter_cart_products_in_the_cart_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="products_in_the_cart",
            field=models.ManyToManyField(
                blank=True,
                through="shop_app.DescriptionProductCart",
                to="shop_app.product",
            ),
        ),
        migrations.AlterField(
            model_name="wishlist",
            name="products_in_the_preferences",
            field=models.ManyToManyField(blank=True, to="shop_app.product"),
        ),
    ]