"""
This following file contains all queries related to a particular model.
"""

from typing import Type

from django.db.models.manager import BaseManager

from HMS.domain.user.models import User, UserFactory


class UserServices:
    """
    This creates model service that provide abstract layer over
    a model, and user has to access service layer instead of an accessing model.
    """

    def get_user_factory(
            self,
    ) -> Type[UserFactory]:
        return UserFactory

    def get_user_repo(self) -> BaseManager[User]:
        return User.objects

    @staticmethod
    def get_user_by_id(user_id: str) -> Type[User]:
        return User.objects.get(id=user_id)
