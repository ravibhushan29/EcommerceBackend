from rest_framework import serializers

from cart.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('id', 'user', 'total_price', 'is_checkout')


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('id', 'product_variant')


class CartItemUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('id', 'quantity')
