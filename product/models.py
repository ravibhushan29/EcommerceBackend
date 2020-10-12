from django.db import models
from common.models import BaseModel


class AttributeBase(BaseModel):
    label = models.CharField(max_length=255) # e.g. color, size, shape, etc.


class Attribute(BaseModel):
    base = models.ForeignKey('AttributeBase', related_name='attributes')
    value = models.CharField(max_length=255) # red , 15 , medium , large


class Product(BaseModel):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.FloatField()


class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT)
    stock = models.PositiveIntegerField()