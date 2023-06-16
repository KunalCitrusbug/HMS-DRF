"""
This file defines the structure of stored data,
including the field types and possibly related information
"""

import uuid
from dataclasses import dataclass

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

    NURSE = "Nurse"
    ADMINISTRATOR = "Administrator"
    PHARMACIST = "Pharmacist"

    STAFF_TYPE = (
        (NURSE, 'Nurse'),
        (ADMINISTRATOR, 'Administrator'),
        (PHARMACIST, 'Pharmacist')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    staff_type = models.CharField(max_length=150, choices=STAFF_TYPE, null=True, blank=True)

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
        db_table = "staff"

    def __str__(self):
        return f"Staff Name: {self.user.name} - Staff Type: {self.get_staff_type_display()}"


class StaffFactory:
    """
    This following class is a Factory method of an above-mentioned model.
    """

    @staticmethod
    def build_entity(id: StaffID, user: User, staff_type: str) -> Staff:
        return Staff(id=id, user=user, staff_type=staff_type)

    @classmethod
    def build_entity_with_id(cls, user: User, staff_type: str) -> Staff:
        entity_id = StaffID(uuid.uuid4())
        return cls.build_entity(id=entity_id.value, user=user, staff_type=staff_type)
