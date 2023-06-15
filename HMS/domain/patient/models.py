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

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, null=True, blank=True)
    contact_no = models.CharField(max_length=12, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        db_table = "patient"

    def __str__(self):
        return self.name


class PatientFactory:
    """
    This following class is a Factory method of an above-mentioned model.
    """

    @staticmethod
    def build_entity(id: PatientID, name: str, user: User, dob: datetime, gender: str, contact_no: str,
                     address: str) -> Patient:
        return Patient(id=id, user=user, name=name, dob=dob, gender=gender, contact_no=contact_no,
                       address=address)

    @classmethod
    def build_entity_with_id(cls, name: str, user: User, dob: datetime, gender: str, contact_no: str,
                             address: str) -> Patient:
        entity_id = PatientID(uuid.uuid4())
        return cls.build_entity(id=entity_id.value, user=user, name=name, dob=dob, gender=gender, contact_no=contact_no,
                                address=address)
