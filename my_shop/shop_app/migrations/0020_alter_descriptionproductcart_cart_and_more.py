# Generated by Django 4.1.1 on 2022-10-31 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0019_alter_checkout_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descriptionproductcart',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_description', to='shop_app.cart'),
        ),
        migrations.AlterField(
            model_name='descriptionproductcart',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_description', to='shop_app.product'),
        ),
        migrations.RemoveField(
            model_name='profile',
            name='history_of_buy',
        ),
        migrations.AddField(
            model_name='profile',
            name='history_of_buy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checkouts', to='shop_app.checkout'),
        ),
    ]
