
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if value < 1900 or value > current_year:
        raise ValidationError(
            'Неверно указан год, не может быть меньше 1900 и больше текущего.'
        )
