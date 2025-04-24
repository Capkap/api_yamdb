import datetime as dt

from django.core.exceptions import ValidationError

from api_yamdb import constants


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError(
            'Год произведения не может быть больше текущего.'
        )


def validate_score_range(value):
    is_valid = constants.MIN_SCORE <= value <= constants.MAX_SCORE
    if not is_valid:
        raise ValidationError(
            f'Оценка должна быть в диапазоне '
            f'от {constants.MIN_SCORE} до {constants.MAX_SCORE}'
        )
    return value
