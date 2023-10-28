import re

from django.core.exceptions import ValidationError


def validate_slug(tag):
    if re.search(r'^[-a-zA-Z0-9_]+$', tag) is None:
        raise ValidationError(
            f'Не допустимые символы <{tag}> в тэге.'
        )


def validate_color(color):
    if re.search(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color) is None:
        raise ValidationError(
            f'Цвет - {color} не соотвествует HEX формату.'
        )
