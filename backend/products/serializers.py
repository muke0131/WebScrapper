from rest_framework import serializers
from .models import Product, SKU


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['color', 'size']


class ProductSerializer(serializers.ModelSerializer):
    available_skus = SKUSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'url', 'title', 'price', 'mrp', 'last_7_day_sale', "fit",
                  "fabric",
                  "neck",
                  "sleeve",
                  "pattern",
                  "length", 'description', 'available_skus']
