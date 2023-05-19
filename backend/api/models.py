from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()


class Tag(models.Model):
    '''Тег -выбор из предустановленных.
    Можно установить несколько тегов на один рецепт.
    Поля Название, цветовой HEX-код, slug.'''
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название тега',
        help_text='Название тега',
    )
    color = ColorField(
        format='hex',
        max_length=7,
        default='#С0С0С0',
        verbose_name='Цвет в hex-формате',
        help_text='Цвет в hex-формате',
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Slug',
        help_text='Slug тега',
        validators=[RegexValidator(regex=r'^[\w.@+-]+$',
                    message='Запрещенные символы в имени')]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''Ингридиенты рецепта.
    Содержат обязательные поля:
    название, количество, единицы измерения.
    '''
    name = models.CharField(
        db_index=True,
        max_length=200,
        verbose_name='Название ингридиента',
        help_text='Название ингредиента',
    )
    measurement_unit = models.CharField(
        default='г',
        max_length=200,
        verbose_name='Единицы измерения',
        help_text='Единицы измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Рецепт содержит обязательные поля.
    Автор(пользователь), название, картинка,
    текстовое описание, ингредиенты, тег (или несколько из предустановленных)
    Время приготовления в минутах.
    '''
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        help_text='Теги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации',
        help_text='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Ингредиенты  для блюда',
        help_text='Ингредиенты для блюда',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Название рецепта',
    )
    image = models.ImageField(
        verbose_name='Фото блюда',
        help_text='Фото блюда',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, 'Время приготовления не может быть меньше 1 минуты!'
            )
        ],
        default=1,
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания рецепта',
        help_text='Введите дату создания рецепта',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_ingredient',
        verbose_name='Ингредиент',
        help_text='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_ingredient',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, 'Количество ингредиентов не может быть меньше 1!'
            ),
            MaxValueValidator(
                1000, 'Количество ингредиентов не может быть больше 1000!'
            )
        ],
        default=1,
        verbose_name='Количество',
        help_text='Количество',
    )

    class Meta:
        verbose_name = 'Кол-во ингредиентов'
        verbose_name_plural = 'Кол-во ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe',
            )
        ]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Избранный автор',
        help_text='Избранный автор',
    )

    class Meta:
        verbose_name = 'Избранный автор'
        verbose_name_plural = 'Избранные авторы'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                name="Ограничение на самоподписку",
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.author}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_list',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Избранный рецепт',
        help_text='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorites'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт в списке покупок',
        help_text='Рецепт в списке покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
