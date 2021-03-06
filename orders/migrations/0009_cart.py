# Generated by Django 2.1.5 on 2020-05-22 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_menu_type_display_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('basket', models.CharField(max_length=500)),
            ],
        ),
    ]
