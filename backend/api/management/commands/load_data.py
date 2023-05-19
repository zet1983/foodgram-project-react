import json
import os

from django.core.management.base import BaseCommand

from api.models import Ingredient


class Command(BaseCommand):
    help = 'Add data to db'

    def handle(self, *args, **options):
        # Получить путь к текущему файлу
        current_file_path = os.path.abspath(__file__)

        # Получить родительскую директорию файла
        parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))))))
        file_name = os.path.join(parent_directory, 'data', 'ingredients.json')
        with open(file_name, encoding="utf-8") as file:
            data = json.load(file)

        for ingredient in data:
            name = ingredient['name']
            measurement_unit = ingredient['measurement_unit']
            Ingredient.objects.create(name=name,
                                      measurement_unit=measurement_unit)
