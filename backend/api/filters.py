import django_filters
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

from recipes.models import Recipes

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'


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

    def _filter_related(self, queryset, value, related_manager):
        if value and not self.request.user.is_anonymous:
            recipe_ids = related_manager.values_list(
                'recipe', flat=True
            )
            return queryset.filter(id__in=recipe_ids)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        return self._filter_related(
            queryset, value, self.request.user.favorites
        )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self._filter_related(
            queryset, value, self.request.user.shopping_cart
        )
