from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.OrderView.as_view()),
    path('plan', views.PlanView.as_view(), name='plan'),
    path('new_plan', views.PlanView.as_view(), name='new_plan')
]
