# Generated by Django 4.1.1 on 2022-10-26 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0011_alter_checkout_price_alter_checkout_product_to_buy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='number',
            field=models.IntegerField(default=960021555),
        ),
    ]
