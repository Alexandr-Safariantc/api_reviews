from datetime import datetime

from django.core.exceptions import ValidationError


def check_rate(value: int):
    """Return error if score is out of range."""
    if value not in range(1, 11):
        raise ValidationError(
            message='Ожидается оценка по шкале от 1 до 10'
        )
    return value


def check_year(value: int):
    """Return error if title creation year greater than current one."""
    if value > datetime.now().year:
        raise ValidationError(
            message='Год создания произведения не может быть больше текущего'
        )
    return value
