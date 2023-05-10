# Generated by Django 4.1.1 on 2022-10-30 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop_app", "0015_remove_checkout_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comments",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shop_app.product"
            ),
        ),
        migrations.AlterField(
            model_name="comments",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shop_app.profile"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="cart",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="shop_app.cart"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="wish_list",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="shop_app.wishlist"
            ),
        ),
    ]