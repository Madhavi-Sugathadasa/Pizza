# Generated by Django 2.1.5 on 2020-05-18 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200518_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu_item',
            name='image',
            field=models.ImageField(upload_to='Media'),
        ),
    ]
