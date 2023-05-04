# Generated by Django 4.1.1 on 2022-10-30 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop_app", "0016_alter_comments_product_alter_comments_profile_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="descriptionproductcart",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="shop_app.product",
            ),
        ),
        migrations.AlterField(
            model_name="descriptionproductcart",
            name="quality",
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="coupon_history",
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
