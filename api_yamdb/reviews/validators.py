import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Неверно указан год,'
            ' произведение не может быть написано в будущем. Марти ты ли это?'
        )


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Нельзя использовать значение me в username'
        )
    if not bool(re.match(r'^[\w.@+-]+$', value)):
        raise ValidationError(
            'В поле username можно использовать только буквы,'
            'цифры и символы @/./+/-/_ only'
        )
    return value
