from django.db import models


class Resept(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        "User",
        verbose_name=_("автор"), 
        on_delete=models.CASCADE, 
        related_name='resepts'
    )
    title = models.CharField(_(""), max_length=50, nott_null=True)
    photo = models.ImageField(upload_to='', blank=True)
    discription = models.CharField(_(""), max_length=1000)
    ingredients = models.ForeignKey("Ingredient", verbose_name=_(""), on_delete=models.CASCADE)
    tegs = models.ManyToManyField("Tag", verbose_name=_(""))
    cooking_time = models.PositiveIntegerField(_(""))

    class Meta:
        verb")
        verbose_nams")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        re_detail", kwargs={"pk": self.pk})


class Tag(models.Model):
    title = models.CharField(_(""), max_length=50)
    color_code = models.CharField(_(""), max_length=50)
    # тут надо хранить rgb code
    slug = models.SlugField(_(""))

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    title = models.CharField(_(""), max_length=50)
    amount = models.PositiveIntegerField(_(""))
    unit = models.CharField(_(""), max_length=50)
    

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="following"
    )

    def clean(self) -> None:
        if self.following == self.user:
            raise ValidationError("Нельзя сотворить здесь!")

    def __str__(self) -> str:
        return f'{self.user} follows {self.following}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following_user_following'
            )
        ]