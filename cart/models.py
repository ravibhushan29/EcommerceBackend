from django.db import models
from common.models import BaseModel
from product.models import ProductVariant
from user_management.models import UserProfile


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    is_checkout = models.BooleanField(default=False)
    address = models.TextField()

    class Meta:
        ordering = ('-created_on',)