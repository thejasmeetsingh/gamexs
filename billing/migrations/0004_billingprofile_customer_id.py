# Generated by Django 2.2.2 on 2019-10-26 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_remove_billingprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='customer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]