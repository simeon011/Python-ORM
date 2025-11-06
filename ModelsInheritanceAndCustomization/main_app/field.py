from django.core.exceptions import ValidationError
from django.db import models

class StudentIDField(models.PositiveIntegerField):
    INVALID_INPUT_ERROR_MSG = "Invalid input for student ID"

    def to_python(self, value):
        try:
            return super().to_python(value)
        except ValidationError:
            raise ValueError(self.INVALID_INPUT_ERROR_MSG)

    def get_prep_value(self, value) -> int:
        try:
            value = super().get_prep_value(value)
        except ValueError as e:
            raise e.__class__(self.INVALID_INPUT_ERROR_MSG) from e

        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")

        return value

class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        if not value.isalpha():
            raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return f"****-****-****-{value[-4:]}"
