# Документация к API Foodgram

![example workflow](https://github.com/zet1983/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Описание проекта:

API Foodgram позволяет сохранять свои рецепты и делиться ими с друзьями. Дополнительные возможности позволяют выбрать
 избранные рецепты или подписаться на друзей, можно собрать корзину и выгрузить список того что требуется купить для их
 приготовления.

#### Данные сервера для проверки работы

http://yap.sytes.net
логин: admin@sytes.net
пароль: foodgram

Стек технологий:
 **Python 3.9,
 [Django 3.2.9](https://docs.djangoproject.com/en/4.0/),
 [DjangoRestFramework](https://www.django-rest-framework.org),
 [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/),
 [PostgreSQL](https://www.postgresql.org/docs/),
 [Docker](https://docs.docker.com/),
 [Docker Compose](https://docs.docker.com/compose/),
 [Gunicorn](https://docs.gunicorn.org/en/stable/) 20.0,
 [Nginx](https://docs.nginx.com/) 1.21 ([Ru](https://nginx.org/ru/docs/)).**

## Особенность данного проекта:

В этом проекте применена технология Single-page application. 
Моя работа заключалась в написании Backend API и размещение всего проекта на сервере.

Джанго настроен для работы с базой данных Postgres.

Образ серверной части приложения создаётся в момент размещения кода в репозитории GitHub. Для этого создан
 соответствующий скрипт с активацией по команде push в ветку main.

Следующим шагом происходит сборка docker образа и его деплой на DockerHub.

После успешного деплоя происходит отправка отчёта от GitHub в телеграмм разработчика.

Запуск проекта происходит с применением docker-compose (описано ниже). При этом происходит сборка четырёх образов:
1) Компиляция по соответствующим инструкциям образа фронтэнда из докерфайла.
2) Копирование с DockerHub образа Postgres на базе Alpine Linux и копирование туда файлов базы данных.
3) Копирование с DockerHub бэкэнд образа [zet1983/foodgram] скомпилированного автоматически GitHub-ом.
4) Копирование с DockerHub бэкэнд образа Nginx на базе Alpine Linux, его настройка для работы со статикой и бекендом.

## Как запустить проект:

Надо написать после раскатки на сервере как это сделать

## Работа с эндпоинтами:

Краткое описание основных возможностей, за более подробной информацией
 обратитесь к [/redoc/](https://github.com/zet1983/foodgram-project-react/tree/master/docs/redoc.html) 
 ([yml](https://github.com/zhss1983/foodgram-project-react/tree/master/docs/openapi-schema.yml)). 
