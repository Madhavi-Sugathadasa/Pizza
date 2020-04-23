# Generated by Django 2.1.5 on 2020-05-24 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order_order_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='size',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
