# Generated by Django 4.1.1 on 2022-10-26 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0010_checkout_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='product_to_buy',
            field=models.ManyToManyField(blank=True, null=True, to='shop_app.product'),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop_app.profile'),
        ),
    ]
