import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['name', 'price']
