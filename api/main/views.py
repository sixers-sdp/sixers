from django.views.generic import ListView
from . import models


class OrderView(ListView):
    queryset = models.Order.objects.all()
    context_object_name = 'orders'
    template_name = 'orders.html'