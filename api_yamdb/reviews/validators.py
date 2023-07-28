import re

from django.core.exceptions import ValidationError
from django.utils import timezone

from api.constants import INVALID_SYMBOLS


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Неверно указан год,'
            ' произведение не может быть написано в будущем. Марти ты ли это?'
        )


def validate_username(value):
    banned_chars = ", ".join(set(re.sub(INVALID_SYMBOLS, '', value)))
    if banned_chars:
        raise ValidationError(
            f'Нельзя использовать символы: {banned_chars} в имени')
    if value.lower() == 'me':
        raise ValidationError(
            'Нельзя использовать значение me в имени'
        )
    return value
