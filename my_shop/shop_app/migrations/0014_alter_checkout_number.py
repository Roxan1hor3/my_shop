# Generated by Django 4.1.1 on 2022-10-26 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0013_alter_checkout_number_alter_checkout_product_to_buy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
