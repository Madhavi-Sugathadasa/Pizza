# Generated by Django 2.1.5 on 2020-05-18 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu_Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=64)),
                ('image', models.ImageField(upload_to='uploads/')),
                ('no_of_toppings', models.IntegerField(default=0)),
                ('is_mult_cat', models.BooleanField(default=False)),
                ('small_price', models.FloatField()),
                ('large_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Menu_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='menu_item',
            name='type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_types', to='orders.Menu_Type'),
        ),
    ]
