from django.views.generic import ListView, TemplateView

# from map.utils import map_text
from . import models


class OrderView(ListView):
    queryset = models.Order.objects.all()
    context_object_name = 'orders'
    template_name = 'orders.html'


class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        # c['map_text'] = map_text
        return c
