from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

from .validators import validate_slug


User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты."""

    name = models.CharField(
        max_length=200, 
        verbose_name='Название ингредиента', 
        blank=False, 
        null=False,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        blank=True,
        null=True,
    )
    amount = models.SmallIntegerField(
        validators=[MaxValueValidator(1000)],
        blank=True,
        null=True,
    )

    class Meta:
        """Мета класс."""

        verbose_name = ("Ингредиент")
        verbose_name_plural = ("Ингредиенты")

    def __str__(self):
        """Строковое представление названия ингредиента."""
        return self.name


class Tag(models.Model):
    """Тэги."""

    name = models.CharField(
        max_length=200,
        verbose_name='название тэга',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='rgb код',
        null=True,
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='поле слаг',
        null=True,
        unique=True,
        validators=[validate_slug]
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name="тэг",
    )

    class Meta:
        """Мета класс."""

        verbose_name = ("Тэг")
        verbose_name_plural = ("Тэги")

    def __str__(self):
        """Строковое представление названия тэга."""
        return self.name


class Recipe(models.Model):
    """Рецепты."""

    author = models.ForeignKey(
        User,
        verbose_name="автор", 
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название рецепта',
        unique=True,
        db_index=True,
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Фотография блюда',
        null=True,
        default=None,
    )
    text = models.CharField(
        max_length=1000,
        verbose_name='Описание рецепта',
        null=True,
        default=None,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="ингредиент",
        through='RecipeIngredients'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления'
    )
    is_favorited = models.BooleanField(
        verbose_name='является ли избранным'
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='находится ли в корзине'
    )

    class Meta:
        """Мета класс."""

        verbose_name = ("рецепт")
        verbose_name_plural = ("рецепты")

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Связывающая модель для ManyToMany."""

    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепты'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиенты'
    )

    class Meta:
        """Мета класс."""

        verbose_name = ("Ингредиент-рецепт")
        verbose_name_plural = ("Ингредиенты-рецепты")


class Follow(models.Model):
    """Подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='подписка',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='подписчик'
    )

    class Meta:
        """Мета класс."""

        verbose_name = ("Подписка")
        verbose_name_plural = ("Подписки")

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following_user_following'
            )
        ]

    def clean(self) -> None:
        if self.following == self.user:
            raise ValidationError("Нельзя сотворить здесь!")

    def __str__(self) -> str:
        """Строковое представление модели подписок."""
        return f'{self.user} follows {self.following}'


class Purchase(models.Model):
    """Покупки пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="пользователь"
    )

    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="рецепты"
    )

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
