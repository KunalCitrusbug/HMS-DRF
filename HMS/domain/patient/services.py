"""
This following file contains all queries related to particular model.
"""

from typing import Type

from django.db.models.manager import BaseManager

from HMS.domain.patient.models import Patient, PatientFactory


class PatientServices:
    """
    This creates model service that provide abstract layer over
    model and user have to access service layer instead of accessing model.
    """

    def get_patient_factory(
            self,
    ) -> Type[PatientFactory]:
        return PatientFactory

    def get_patient_repo(self) -> BaseManager[Patient]:
        return Patient.objects

    @staticmethod
    def get_patient_by_id(patient_id: str) -> Type[Patient]:
        return Patient.objects.get(id=patient_id)
