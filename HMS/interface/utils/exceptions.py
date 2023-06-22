from rest_framework.exceptions import ValidationError


class InvalidPasswordException(ValidationError):
    pass


