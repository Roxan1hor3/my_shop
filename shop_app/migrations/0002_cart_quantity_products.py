# Generated by Django 4.1.1 on 2022-10-23 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="quantity_products",
            field=models.TextField(blank=True, default="0", null=True),
        ),
    ]
