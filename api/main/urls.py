from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.OrderView.as_view()),
    path('order/state/<int:id>', views.OrderChangeStateView.as_view(), name='change_order_state'),
    path('cancel/state/<int:id>', views.CancellationChangeStateView.as_view(), name='change_cancel_state'),
    path('order/edit/<int:pk>', views.OrderEditView.as_view(), name='order_edit'),
    path('plan', views.PlanView.as_view(), name='plan'),
    path('new_plan', views.NewPlanView.as_view(), name='new_plan'),
    path('video', views.VideoView.as_view(), name='video'),
]
