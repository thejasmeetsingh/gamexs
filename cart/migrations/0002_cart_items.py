# Generated by Django 2.2.2 on 2019-08-28 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
