# Generated by Django 3.0.4 on 2020-05-04 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0005_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users/'),
        ),
    ]