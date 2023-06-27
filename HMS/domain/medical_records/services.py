"""
This following file contains all queries related to particular model.
"""

from typing import Type

from django.db.models.manager import BaseManager

from HMS.domain.medical_records.models import MedicalRecord, MedicalRecordFactory
from HMS.domain.staff.models import Staff, StaffFactory


class MedicalRecordServices:
    """
    This creates model service that provide abstract layer over
    a model, and user has to access service layer instead of an accessing model.
    """

    def get_medical_record_factory(
            self,
    ) -> Type[MedicalRecordFactory]:
        return MedicalRecordFactory

    def get_medical_record_repo(self) -> BaseManager[MedicalRecord]:
        return MedicalRecord.objects

    @staticmethod
    def get_medical_record_by_id(id: str) -> Type[MedicalRecord]:
        return MedicalRecord.objects.get(id=id)
