from django.db import models
from common.models import BaseModel


class AttributeBase(BaseModel):
    label = models.CharField(max_length=255) # e.g. color, size, shape, etc.


class Attribute(BaseModel):
    base = models.ForeignKey('AttributeBase', related_name='attributes', on_delete=models.PROTECT)
    value = models.CharField(max_length=255) # red , 15 , medium , large


class Product(BaseModel):
    name = models.CharField(max_length=256)
    description = models.TextField()


class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    ready_for_sale = models.BooleanField(default=False)