from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet

from albert_api.serializers import LocationUpdateSerializer, DotAssociationSerializer, CancellationSerializer
from main.models import Product, Order, ExecutionPlan, PLAN_STATE_NEW, LocationUpdate, DotAssociation, Cancellation
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
        # try:
        #     instance = self.queryset.filter(state=PLAN_STATE_NEW).latest()
        # except ExecutionPlan.DoesNotExist:
        instance = ExecutionPlan.create_new()
        if not instance:
            return Response(status=HTTP_204_NO_CONTENT)

        # if instance.state != PLAN_STATE_NEW:
        #     instance = ExecutionPlan.create_new()
        #     if not instance:
        #         return Response(status=HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LocationUpdateViewSet(viewsets.ModelViewSet):
    queryset = LocationUpdate.objects.all()
    serializer_class = LocationUpdateSerializer


class DotAssociationViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = DotAssociation.objects.all()
    serializer_class = DotAssociationSerializer


class CancellationViewSet(viewsets.ModelViewSet):
    queryset = Cancellation.objects.all()
    serializer_class = CancellationSerializer
