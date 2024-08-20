import json
from django.core.management.base import BaseCommand
from products.models import Product, SKU


class Command(BaseCommand):
    help = 'Load product data into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        with open(options['json_file'], 'r') as file:
            data = json.load(file)
            for item in data:
                product_data = {
                    'category': item.get('category'),
                    'url': item.get('url'),
                    'title': item.get('title'),
                    'price': item.get('price'),
                    'mrp': item.get('mrp'),
                    'last_7_day_sale': item.get('last_7_day_sale'),
                    'fit': item.get('fit'),
                    'fabric': item.get('fabric'),
                    'neck': item.get('neck'),
                    'sleeve': item.get('sleeve'),
                    'pattern': item.get('pattern'),
                    'length': item.get('length'),
                    'description': item.get('description'),
                }
                product, created = Product.objects.update_or_create(
                    url=product_data['url'],
                    defaults=product_data
                )
                for sku in item.get('available_skus', []):
                    SKU.objects.update_or_create(
                        product=product,
                        color=sku['color'],
                        size=sku['size'],
                    )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
