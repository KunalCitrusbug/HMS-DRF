"""
This following file contains all queries related to a particular model.
"""

from typing import Type

from django.db.models.manager import BaseManager

from HMS.domain.doctor.models import Doctor, DoctorFactory


class DoctorServices:
    """
    This creates model service that provide abstract layer over
    a model, and user has to access service layer instead of an accessing model.
    """

    def get_doctor_factory(
            self,
    ) -> Type[DoctorFactory]:
        return DoctorFactory

    def get_doctor_repo(self) -> BaseManager[Doctor]:
        return Doctor.objects

    @staticmethod
    def get_doctor_by_id(id: str) -> Type[Doctor]:
        return Doctor.objects.get(id=id)
