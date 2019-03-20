from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'plans', views.PlanView)
router.register(r'location', views.LocationUpdateViewSet)
router.register(r'dots', views.DotAssociationViewSet)



app_name = 'albert_api'

urlpatterns = [
    path('', include(router.urls)),
    # path('plan', views.PlanView.as_view())
]
