from django.db import models
from django.db.models import Sum

from common.models import BaseModel
from product.models import ProductVariant
from user_management.models import UserProfile


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_products')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        self.item_total = self.product_variant.price * self.quantity
        super(CartItem, self).save(*args, **kwargs)


class Cart(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    is_checkout = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_on',)

    def save(self, *args, **kwargs):
        self.total_price = self.cart_products.all().aggregate(Sum('item_total'))['item_total__sum']
        super(Cart, self).save(*args, **kwargs)