# Generated by Django 3.0.4 on 2020-04-03 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dinner_Platter_c',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Pasta_salad_c',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_c',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('toppings', models.ManyToManyField(blank=True, to='orders.Topping')),
            ],
        ),
        migrations.CreateModel(
            name='Sicilian_Pizza_c',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('name', models.CharField(max_length=64)),
                ('toppings', models.ManyToManyField(blank=True, to='orders.Topping')),
            ],
        ),
        migrations.CreateModel(
            name='Regular_Pizza_c',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('name', models.CharField(max_length=64)),
                ('toppings', models.ManyToManyField(blank=True, to='orders.Topping')),
            ],
        ),
    ]
