from rest_framework import serializers

from main.models import Order, Product, ExecutionPlan, LocationUpdate, DotAssociation, Cancellation


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = []


class OrderSerializer(serializers.ModelSerializer):
    # products = ProductSerializer()
    device_id = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = ['products_text', 'table_number', 'products', 'device_id', 'state']
        # write_only_fields = ['device_id']

        extra_kwargs = {
            'table_number': {'read_only': True},
        }

    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        table_num = DotAssociation.objects.get(dot_id=device_id).location
        validated_data['table_number'] = table_num
        order = super().create(validated_data)
        return order

class PlanSerializer(serializers.ModelSerializer):
    steps = serializers.JSONField(source='plan_as_json', read_only=True)

    class Meta:
        model = ExecutionPlan
        exclude = ['plan_parsed']
        extra_kwargs = {
            'id': {'read_only': True},
            'plan_parsed': {'read_only': True},
            'steps': {'read_only': True},
        }


class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationUpdate
        exclude = []


class DotAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DotAssociation
        exclude = []


class CancellationSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(write_only=True)

    class Meta:
        model = Cancellation
        exclude = []

        extra_kwargs = {
            'table_number': {'read_only': True},
        }

    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        table_num = DotAssociation.objects.get(dot_id=device_id).location
        validated_data['table_number'] = table_num
        order = super().create(validated_data)
        return order
