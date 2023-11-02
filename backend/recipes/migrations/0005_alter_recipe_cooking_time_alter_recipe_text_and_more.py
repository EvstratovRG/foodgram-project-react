# Generated by Django 4.2.6 on 2023-11-02 19:21

import django.core.validators
from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_remove_recipe_is_favorited_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(default=None, null=True, verbose_name='Описание рецепта'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, null=True, validators=[recipes.validators.validate_color], verbose_name='rgb код'),
        ),
    ]
