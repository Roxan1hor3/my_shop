# Generated by Django 4.1.1 on 2022-10-26 10:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop_app", "0006_profile_count_product_in_cart_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="checkout",
            old_name="county",
            new_name="country",
        ),
    ]
