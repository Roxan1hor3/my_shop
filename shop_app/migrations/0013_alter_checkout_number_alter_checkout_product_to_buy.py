# Generated by Django 4.1.1 on 2022-10-26 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop_app", "0012_checkout_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="checkout",
            name="number",
            field=models.IntegerField(default=722405036),
        ),
        migrations.AlterField(
            model_name="checkout",
            name="product_to_buy",
            field=models.ManyToManyField(blank=True, to="shop_app.product"),
        ),
    ]
