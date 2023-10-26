from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from .validators import validate_slug

User = get_user_model()


class BaseFoodgramModel(models.Model):
    """Абстрактная модель."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ingredient(BaseFoodgramModel):
    """Ингредиенты."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        blank=False,
        null=False,
        db_index=True,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        blank=True,
        null=True,
    )

    class Meta:
        """Мета класс."""

        ordering = ['name']
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        """Строковое представление названия ингредиента."""
        return f'{self.name} {self.measurement_unit}'


class Tag(BaseFoodgramModel):
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

    class Meta:
        """Мета класс."""

        unique_together = ('name', 'slug')
        ordering = ['name']
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        """Строковое представление названия тэга."""
        return self.name


class Recipe(BaseFoodgramModel):
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
        db_index=True,
    )
    image = models.ImageField(
        upload_to='recipes/',
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
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='тэги',
        through='RecipeTag'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления'
    )

    class Meta:
        """Мета класс."""

        ordering = ['name']
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"

    def __str__(self):
        return self.name


class RecipeIngredient(BaseFoodgramModel):
    """Связывающая модель для ManyToMany."""

    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепты',
        related_name='recipe_ingredients',
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиенты',
        related_name='recipe_ingredients',
    )
    amount = models.SmallIntegerField(
        validators=[MaxValueValidator(1000)],
        blank=True,
        null=True,
    )

    class Meta:
        """Мета класс."""

        ordering = ['created_at']
        verbose_name = "Ингредиент-рецепт"
        verbose_name_plural = "Ингредиенты-рецепты"

    def __str__(self):
        return f'{self.recipes} - {self.ingredients}, {self.amount}.'


class Follow(BaseFoodgramModel):
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
        verbose_name='подписчик',
    )

    class Meta:
        """Мета класс."""

        ordering = ['user']
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following_user_following'
            )
        ]

    def clean(self) -> None:
        if self.following == self.user:
            raise ValidationError("Нельзя подписаться на самого себя!")

    def __str__(self) -> str:
        """Строковое представление модели подписок."""
        return f'{self.user} подписан на {self.following}'


class Purchase(BaseFoodgramModel):
    """Покупки пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="пользователь",
    )

    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="рецепты",
    )

    class Meta:
        """Мета класс."""
        ordering = ['user']
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"


class Favorite(BaseFoodgramModel):
    """Избранные рецепты пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="пользователь",
    )

    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="рецепты",
    )

    class Meta:
        """Мета класс."""
        ordering = ['user']
        verbose_name = "избранное"
        verbose_name_plural = "избранные"

    def __str__(self):
        return f'{self.user} likes {self.recipes}'


class RecipeTag(BaseFoodgramModel):
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        """Мета класс."""
        ordering = ['created_at']
        verbose_name = "Тэг рецепта"
        verbose_name_plural = "Теги рецептов"

    def __str__(self):
        return f'{self.recipes} {self.tags}'
