from django.contrib.auth import get_user_model
import django_filters
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipes

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'
    # name = django_filters.CharFilter(
    #     field_name='name',
    #     lookup_expr='istartswith'
    # )

    # class Meta:
    #     model = Ingredient
    #     fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'author',)