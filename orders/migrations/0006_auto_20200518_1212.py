# Generated by Django 2.1.5 on 2020-05-18 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200518_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu_item',
            name='large_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='menu_item',
            name='small_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
