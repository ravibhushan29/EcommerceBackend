from django.urls import path
from product.views import ProductView, ProductDetailUpdateView, ProductVariantView, ProductVariantDetailUpdateView

urlpatterns = [
    path('product/', ProductView.as_view()),
    path('product/<str:pk>', ProductDetailUpdateView.as_view()),
    path('product-variant/', ProductView.as_view()),
    path('product-variant/<str:pk>', ProductDetailUpdateView.as_view()),
    ]
