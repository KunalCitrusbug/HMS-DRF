"""
This file define the structure of stored data,
including the field types and possibly related information
"""

import uuid
from dataclasses import dataclass
from datetime import datetime

from django.db import models

from HMS.domain.activity.models import Activity
from HMS.domain.user.models import User


@dataclass(frozen=True)
class PatientID:
    """
    This is a value object that should be used to generate and pass the
    PatientID to the Patient
    """

    value: uuid.UUID


class Patient(Activity):
    """
    This Following model will contain the database structure of
    Patient tabel.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    dob = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        db_table = "patient"

    def __str__(self):
        return self.user.name


class PatientFactory:
    """
    This following class is a Factory method of an above-mentioned model.
    """

    @staticmethod
    def build_entity(id: PatientID, user: User, age: int, dob: datetime) -> Patient:
        return Patient(id=id, user=user, age=age, dob=dob)

    @classmethod
    def build_entity_with_id(cls, user: User, age: int, dob: datetime) -> Patient:
        entity_id = PatientID(uuid.uuid4())
        return cls.build_entity(id=entity_id.value, user=user, age=age, dob=dob)
