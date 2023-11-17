from django.urls import path
from . import views
from .views import CtrAPIView, EvpmAPIView, AggregationAPIView

urlpatterns = [
    path('', CtrAPIView.as_view(), name='ctr'),
    path('evpm', EvpmAPIView.as_view(), name='evpm'),
    path('aggregation-tables', AggregationAPIView.as_view(), name='aggregation'),
]
