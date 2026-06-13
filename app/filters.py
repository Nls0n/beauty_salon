from django_filters import rest_framework as filters
from .models import Service

class ServiceFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    title_contains = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Service
        fields = ['category']