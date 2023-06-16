"""
This file defines the structure of stored data,
including the field types and possibly related information
"""

import uuid
from dataclasses import dataclass

from django.db import models

from HMS.domain.activity.models import Activity


@dataclass(frozen=True)
class SpecializationID:
    """
    This is a value object that should be used to generate and pass the
    PatientID to the Patient
    """

    value: uuid.UUID


class Specialization(Activity):
    """
    This following class is database structure of Medical Records of Patient.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Specialization"
        verbose_name_plural = "Specializations"
        db_table = "specialization"

    def __str__(self):
        return self.title


class SpecializationFactory:
    """
    This following class is a Factory method of an above-mentioned model.
    """

    @staticmethod
    def build_entity(id: id, specialization: str) -> Specialization:
        return Specialization(id=id, specialization=specialization)

    @classmethod
    def build_entity_with_id(cls, specialization: str) -> Specialization:
        entity_id = SpecializationID(uuid.uuid4())
        return cls.build_entity(id=entity_id, specialization=specialization)
