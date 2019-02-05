from rest_framework import serializers

from main.models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = []


class OrderSerializer(serializers.ModelSerializer):
    # products = ProductSerializer()

    class Meta:
        model = Order
        exclude = []
