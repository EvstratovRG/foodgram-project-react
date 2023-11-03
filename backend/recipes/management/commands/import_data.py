import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag, User
from django.db import transaction

CSV_PATH_INGREDIENTS = os.path.join(settings.BASE_DIR, 'data/ingredients.csv')
CSV_PATH_USERS = os.path.join(settings.BASE_DIR, 'data/users.csv')
CSV_PATH_TAGS = os.path.join(settings.BASE_DIR, 'data/tags.csv')


class Command(BaseCommand):
    help = 'Импорт данных из CSV в модель Ingredient'

    def import_ingredients(self):
        with open(CSV_PATH_INGREDIENTS, newline='', encoding='utf8') as file:
            csv_reader = csv.reader(file)
            data = []
            next(csv_reader)
            for row in csv_reader:
                name, measurement_unit = row
                ingredient = Ingredient(
                    name=name,
                    measurement_unit=measurement_unit,
                )
                data.append(ingredient)
            Ingredient.objects.bulk_create(data)

    def import_users(self):
        with open(CSV_PATH_USERS, newline='', encoding='utf8') as file:
            csv_reader = csv.reader(file)
            data = []
            next(csv_reader)
            for row in csv_reader:
                email, username, first_name, last_name, password = row
                user = User(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                )
                data.append(user)
            User.objects.bulk_create(data)

    def import_tags(self):
        with open(CSV_PATH_TAGS, newline='', encoding='utf8') as file:
            csv_reader = csv.reader(file)
            data = []
            next(csv_reader)
            for row in csv_reader:
                name, color, slug = row
                tag = Tag(name=name, color=color, slug=slug)
                data.append(tag)
            Tag.objects.bulk_create(data)

    @transaction.atomic
    def handle(self, *args, **options):
        self.import_ingredients()
        self.import_users()
        self.import_tags()
        self.stdout.write(self.style.SUCCESS('Импорт завершен'))
