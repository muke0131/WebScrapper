# Generated by Django 5.1 on 2024-08-20 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_sku_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sku',
            name='quantity',
        ),
    ]
