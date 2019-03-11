from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from albert_api.serializers import LocationUpdateSerializer
from main.models import Product, Order, ExecutionPlan, PLAN_STATE_NEW, LocationUpdate
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
        if instance.state != PLAN_STATE_NEW:
            instance = ExecutionPlan.create_new()
            if not instance:
                return Response(status=HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class LocationUpdateViewSet(viewsets.ModelViewSet):
    queryset = LocationUpdate.objects.all()
    serializer_class = LocationUpdateSerializer
