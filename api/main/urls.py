from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.OrderView.as_view()),
    path('order_state/<int:id>', views.OrderChangeStateView.as_view(), name='change_order_state'),
    path('plan', views.PlanView.as_view(), name='plan'),
    path('new_plan', views.NewPlanView.as_view(), name='new_plan'),
]
