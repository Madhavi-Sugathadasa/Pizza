# Generated by Django 2.1.5 on 2020-05-22 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date_time',
            field=models.DateTimeField(),
        ),
    ]
