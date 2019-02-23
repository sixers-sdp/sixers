from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView, RedirectView

# from map.utils import map_text
from . import models


class OrderView(ListView):
    queryset = models.Order.objects.all()
    context_object_name = 'orders'
    template_name = 'orders.html'



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
