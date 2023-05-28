import django_filters
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

from recipes.models import Favorite, Recipes, ShoppingCart

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

    def filter_is_favorited(self, queryset, name, value):
        author = self.request.user
        if value:
            favorite_recipes_ids = Favorite.objects.filter(
                user=author
            ).values('recipe_id')
            return queryset.filter(pk__in=favorite_recipes_ids)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        author = self.request.user
        if value:
            cart_recipes_ids = ShoppingCart.objects.filter(
                user=author
            ).values('recipe_id')
            return queryset.filter(pk__in=cart_recipes_ids)
        return queryset
