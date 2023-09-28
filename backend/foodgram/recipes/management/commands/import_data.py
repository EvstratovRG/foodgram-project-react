import csv

from django.core.management.base import BaseCommand
import os
from recipes.models import Ingredient
from django.conf import settings


CSV_PATH = os.path.join(settings.CSV_PATH, 'data/ingredients.csv')


class Command(BaseCommand):
    help = 'Импорт данных из CSV в модель Ingredient'

    def handle(self, *args, **options):
        with open(CSV_PATH, newline='', encoding='utf8') as file:
            csv_reader = csv.reader(file)
            objects = []
            next(csv_reader)
            for row in csv_reader:
                name, measurement_unit = row
                ingredient = Ingredient(name=name, measurement_unit=measurement_unit)
                objects.append(ingredient)
            Ingredient.objects.bulk_create(objects)

        self.stdout.write(self.style.SUCCESS('Импорт завершен'))
