from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Product, Order, ExecutionPlan
from .serializers import ProductSerializer, OrderSerializer, PlanSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PlanView(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    queryset = ExecutionPlan.objects.all()

    @action(detail=False)
    def latest(self, request):
        instance = self.queryset.latest()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
