from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, RedirectView

# from map.utils import map_text
from main.models import ORDER_STATE_NEW, ORDER_STATE_DELIVERY, ORDER_STATE_READY, ORDER_STATES
from . import models


class OrderView(TemplateView):
    template_name = 'orders.html'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['new_orders'] = models.Order.objects.filter(state=ORDER_STATE_NEW)
        c['ready_orders'] = models.Order.objects.filter(state=ORDER_STATE_READY)
        c['delivery_orders'] = models.Order.objects.filter(state=ORDER_STATE_DELIVERY)
        return c


@method_decorator(login_required, name='dispatch')
class OrderChangeStateView(View):
    template_name = 'orders.html'
    http_method_names = ['post']

    def post(self, request, id, **kwargs):
        state = request.POST.get('state', '')
        if state in ORDER_STATES:
           models.Order.objects.filter(pk=id).update(state=state)

        return HttpResponseRedirect('/')




class PlanView(DetailView):
    """
    Shows current execution plan for the robot.
    """

    template_name = 'plan.html'
    queryset = models.ExecutionPlan.objects.all()
    context_object_name = 'current_plan'

    def get_object(self, queryset=None):
        return self.get_queryset().last()


@method_decorator(login_required, name='dispatch')
class NewPlanView(RedirectView):
    """
    Creates a new plan and redirects user back.
    """
    pattern_name = 'main:plan'
    permanent = False

    def get(self, request, *args, **kwargs):
        models.ExecutionPlan.create_new()

        return super().get(request, *args, **kwargs)
