from django.db.models import Q
import django_filters
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

from recipes.models import Recipes

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'

    def filter_queryset(self, request, queryset, view):
        search_value = request.query_params.get(self.search_param, '')
        if search_value:
            queryset = queryset.filter(Q(name__startswith=search_value))
        return queryset


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
