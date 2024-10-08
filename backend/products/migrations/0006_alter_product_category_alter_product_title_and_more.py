# Generated by Django 5.1 on 2024-08-20 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_sku_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sku',
            name='color',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sku',
            name='size',
            field=models.TextField(blank=True, null=True),
        ),
    ]
