from rest_framework import serializers

from main.models import Order, Product, ExecutionPlan


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = []


class OrderSerializer(serializers.ModelSerializer):
    # products = ProductSerializer()

    class Meta:
        model = Order
        exclude = []


class PlanSerializer(serializers.ModelSerializer):
    steps = serializers.JSONField(source='plan_as_json')


    class Meta:
        model = ExecutionPlan
        exclude = ['plan_out', 'plan_parsed']
