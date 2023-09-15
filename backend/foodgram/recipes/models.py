from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator

from django.core.exceptions import ValidationError


User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты."""

    title = models.CharField(
        max_length=100, 
        verbose_name='Название ингредиента', 
        blank=False, 
        null=False,
    )
    amount = models.PositiveIntegerField(
        validators=[MaxValueValidator(1000)],
        verbose_name='Количество',
        blank=True,
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        blank=True,
    )

    class Meta:
        """Мета класс."""

        db_table = "ingredient"
        verbose_name = ("Ингредиент")
        verbose_name_plural = ("Ингредиенты")

    def __str__(self):
        """Строковое представление названия ингредиента."""
        return self.title


class Tag(models.Model):
    """Тэги."""

    title = models.CharField(
        max_length=50,
        verbose_name='название тэга',
    )
    color_code = models.CharField(
        max_length=50,
        verbose_name='rgb код',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='поле слаг',
    )

    class Meta:
        """Мета класс."""

        verbose_name = ("Тэг")
        verbose_name_plural = ("Тэги")

    def __str__(self):
        """Строковое представление названия тэга."""
        return self.title


class Recipe(models.Model):
    """Рецепты."""

    author = models.ForeignKey(
        User,
        verbose_name="автор", 
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
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
    discription = models.CharField(
        max_length=1000,
        verbose_name='Описание рецепта',
        null=True,
        default=None,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="ингредиент",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    tag = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name="тэг",
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления'
    )

    class Meta:
        """Мета класс."""

        verbose_name = ("рецепт")
        verbose_name_plural = ("рецепты")

    def __str__(self):
        return self.title


class RecipeTag(models.Model):
    """Связывающая модель для ManyToMany."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='тэг'
    )

    class Meta:
        """Мета класс."""

        verbose_name = ("Тэг-рецепт")
        verbose_name_plural = ("Тэги-рецепты")


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
