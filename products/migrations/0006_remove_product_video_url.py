# Generated by Django 2.2.2 on 2019-07-14 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20190714_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='video_url',
        ),
    ]
