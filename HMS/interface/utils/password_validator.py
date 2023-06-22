"""
This is a file that usually contains utility functions, which are small and independent pieces of code that perform
specific tasks.
These functions can be reused throughout the project, making it easier to keep the code organized and maintainable.
"""
import re

from django.conf import settings


def password_validator(password):
    password_pattern = re.compile(settings.PASSWORD_PATTERN)

    try:
        if not password_pattern.match(password):
            return False
        else:
            return True

    except Exception as e:
        raise Exception("Some Error occurred", e)
