"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""
from typing import Any, Dict

from HMS.domain.user.models import User
from HMS.domain.user.services import UserServices
from HMS.interface.utils.exceptions import InvalidPasswordException
from HMS.interface.utils.password_validator import password_validator


class UserAppServices:
    """
    This module provides the application layer service for the Django domain-driven structure.
    It encapsulates the business logic and acts as an intermediary between the presentation layer
    (views) and the domain layer
    (models and repositories).
    """

    def __init__(self):
        self.user_services = UserServices()

    def create_user(self, data: Dict[str, Any]) -> User:
        """
        This method is responsible for creating a new User object based on the provided data
        by accessing the Domain Layer.
        """
        password = data['password']
        email = data['email']
        if not password_validator(password):
            raise InvalidPasswordException("Enter valid password")
        else:
            try:
                user = self.user_services.get_user_factory().build_entity_with_id(
                    email=data['email'],
                    is_active=True,
                    is_admin=False,
                    password=data['password'],
                    name=data['name'],
                    contact_no=data['contact_no'],
                    gender=data['gender'],
                    user_type=data['user_type']
                )
                user.set_password(data['password'])
                user.save()
                return user
            except Exception as e:
                raise Exception("Error")
