from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'cart', 'address')


class OrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'status')
