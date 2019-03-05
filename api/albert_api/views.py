from rest_framework import viewsets

from main.models import Product, Order, ExecutionPlan
from .serializers import ProductSerializer, OrderSerializer, PlanSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PlanView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlanSerializer
    queryset = ExecutionPlan.objects.all()
