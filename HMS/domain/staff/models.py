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
class StaffID:
    """
    This is a value object that should be used to generate and pass the
    PatientID to the Patient
    """

    value: uuid.UUID


class Staff(Activity):
    """
    This following class will contain Staff related information and database structure.
    """

    STAFF_TYPE = (
        ('Nurse', 'Nurse'),
        ('Administrator', 'Administrator'),
        ('Pharmacist', 'Pharmacist')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    staff_type = models.CharField(max_length=150, choices=STAFF_TYPE)
    specialization = models.CharField(max_length=150)
    doj = models.DateField()
    contact_no = models.CharField(max_length=12)

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
        db_table = "staff"

    def __str__(self):
        return str(self.name + self.specialization)


class StaffFactory:
    """
    This following class is a Factory method of above-mentioned model.
    """

    @staticmethod
    def build_entity(id: StaffID, user: User, name: str, staff_type: str, specialization: str, doj: datetime,
                     contact_no: str) -> Staff:
        return Staff(id=id, name=name, user=user, staff_type=staff_type, specialization=specialization, doj=doj,
                     contact_no=contact_no)

    @classmethod
    def build_entity_with_id(cls, user: User, name: str, staff_type: str, specialization: str, doj: datetime,
                             contact_no: str) -> Staff:
        entity_id = StaffID(uuid.uuid4())
        return cls.build_entity(id=entity_id, name=name, user=user, staff_type=staff_type,
                                specialization=specialization, doj=doj,
                                contact_no=contact_no)
