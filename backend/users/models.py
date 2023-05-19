from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import check_username


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Логин',
        help_text='Логин пользователя',
        validators=[check_username,
                    UnicodeUsernameValidator()
                    ]
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Пароль пользователя',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        help_text='Имя пользователя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Фамилия',
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Электронная почта',
        help_text='Адрес электронной почты',
    )
    is_subcribed = models.BooleanField(
        default=False,
        verbose_name='Подписка на автора',
        help_text='Отметьте для подписки на автора',
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
