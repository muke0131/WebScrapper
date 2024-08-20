from django.db import models

# Create your models here.
class Product(models.Model):
    category = models.CharField(max_length=255)
    url = models.URLField()
    title = models.CharField(max_length=255)
    price = models.IntegerField(null=True, blank=True)
    mrp = models.IntegerField(null=True, blank=True)
    last_7_day_sale = models.IntegerField(null=True, blank=True)
    fit= models.TextField(null=True, blank=True)
    fabric= models.TextField(null=True, blank=True)
    neck = models.TextField(null=True, blank=True)
    sleeve = models.TextField(null=True, blank=True)
    pattern = models.TextField(null=True, blank=True)
    length = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['title']

class SKU(models.Model):
    product = models.ForeignKey(Product, related_name='available_skus', on_delete=models.CASCADE)
    color = models.CharField(max_length=255)
    size = models.CharField(max_length=10)

    class Meta:
        ordering = ['color', 'size']