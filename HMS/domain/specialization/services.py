"""
This following file contains all queries related to particular model.
"""

from typing import Type

from django.db.models.manager import BaseManager

from HMS.domain.specialization.models import Specialization


class SpecializationServices:
    """
    This creates model service that provide abstract layer over
    a model, and user has to access service layer instead of an accessing model.
    """

    def get_specialization_factory(
            self,
    ) -> Type[Specialization]:
        return Specialization

    def get_specialization_repo(self) -> BaseManager[Specialization]:
        return Specialization.objects

    @staticmethod
    def get_specialization_by_id(id: str) -> Type[Specialization]:
        return Specialization.objects.get(id=id)
