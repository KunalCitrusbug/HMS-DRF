"""
This following file contains all queries related to particular model.
"""

from typing import Type

from django.db.models.manager import BaseManager

from HMS.domain.staff.models import Staff, StaffFactory


class StaffServices:
    """
    This creates model service that provide abstract layer over
    model and user have to access service layer instead of accessing model.
    """

    def get_staff_factory(
            self,
    ) -> Type[StaffFactory]:
        return StaffFactory

    def get_staff_repo(self) -> BaseManager[Staff]:
        return Staff.objects

    @staticmethod
    def get_staff_by_id(id: str) -> Type[Staff]:
        return Staff.objects.get(id=id)
