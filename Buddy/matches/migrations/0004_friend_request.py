# Generated by Django 3.0.4 on 2020-04-25 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_auto_20200422_2309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=999, null=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send', to='matches.User_info')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receive', to='matches.User_info')),
            ],
        ),
    ]