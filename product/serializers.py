from rest_framework import serializers

from product.models import Product, ProductVariant


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'description')


class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = ('id', 'cart', 'attribute', 'price', 'stock', 'ready_for_sale')
