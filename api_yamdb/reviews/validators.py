
from django.core.exceptions import ValidationError
from django.utils import timezone
import re


def validate_year(value):
    current_year = timezone.now().year
    if value < 1900 or value > current_year:
        raise ValidationError(
            'Неверно указан год, не может быть меньше 1900 и больше текущего.'
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
