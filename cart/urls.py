from django.urls import path
from cart.views import AddItemToCartView, UpdateCartItemView

urlpatterns = [
    path('add-to-cart/', AddItemToCartView.as_view()),
    path('update-cart-item/', UpdateCartItemView.as_view()),
    ]
