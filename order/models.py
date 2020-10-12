from django.db import models

from cart.models import Cart
from common.models import BaseModel
from user_management.models import UserProfile

ORDER_STATUS = (
    ('Placed', 'Placed'),
    ('Accepted', 'Accepted'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)


class Order(BaseModel):
    status = models.CharField(max_length=20,choices=ORDER_STATUS, default='Placed')
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    address = models.TextField()
    order_total = models.DecimalField(max_digits=50, decimal_places=2)

    class Meta:
        ordering = ('-created_on',)



