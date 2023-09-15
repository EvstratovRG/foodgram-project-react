import re

from django.core.exceptions import ValidationError


def validate_slug(tag):
    if re.search(r'^[-a-zA-Z0-9_]+$', tag) is None:
        raise ValidationError(
            f'Не допустимые символы <{tag}> в тэге.'
        )