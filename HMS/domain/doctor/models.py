"""
This file defines the structure of stored data,
including the field types and possibly related information
"""

import uuid
from dataclasses import dataclass

from django.db import models

from HMS.domain.activity.models import Activity
from HMS.domain.specialization.models import Specialization
from HMS.domain.user.models import User


@dataclass(frozen=True)
class DoctorID:
    """
    This is a value object that should be used to generate and pass the
    PatientID to the Patient
    """

    value: uuid.UUID


class Doctor(Activity):
    """
    This following class will contain Staff related information and database structure.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialization = models.ManyToManyField(Specialization, related_name="specialization")

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        db_table = "doctor"

    def __str__(self):
        return self.user.name


class DoctorFactory:
    """
    This following class is a Factory method of an above-mentioned model.
    """

    @staticmethod
    def build_entity(id: DoctorID, user: User, name: str, specialization: Specialization) -> Doctor:
        return Doctor(id=id, user=user, specialization=specialization)

    @classmethod
    def build_entity_with_id(cls, user: User, specialization: Specialization) -> Doctor:
        entity_id = DoctorID(uuid.uuid4())
        return cls.build_entity(id=entity_id.value, user=user, specialization=specialization)
