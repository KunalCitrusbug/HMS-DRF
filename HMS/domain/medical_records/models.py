"""
This file define the structure of stored data,
including the field types and possibly related information
"""

import uuid
from dataclasses import dataclass

from django.db import models

from HMS.domain.activity.models import Activity
from HMS.domain.doctor.models import Doctor
from HMS.domain.patient.models import Patient


@dataclass(frozen=True)
class MedicalRecordID:
    """
    This is a value object that should be used to generate and pass the
    PatientID to the Patient
    """

    value: uuid.UUID


class MedicalRecord(Activity):
    """
    This following class is database structure of Medical Records of Patient.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, unique=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        verbose_name = "MedicalRecord"
        verbose_name_plural = "MedicalRecords"
        db_table = "medical_record"

    def __str__(self):
        return f"Medical Record: {self.id} - Patient: {self.patient} - Doctor: {self.doctor}"


class MedicalRecordFactory:
    """
    This following class is a Factory method of an above-mentioned model.
    """

    @staticmethod
    def build_entity(id: id, patient: Patient, doctor: Doctor,
                     description: str) -> MedicalRecord:
        return MedicalRecord(id=id, patient=patient, doctor=doctor, description=description)

    @classmethod
    def build_entity_with_id(cls, patient: Patient, doctor: Doctor,
                             description: str) -> MedicalRecord:
        entity_id = MedicalRecordID(uuid.uuid4())
        return cls.build_entity(id=entity_id.value, patient=patient, doctor=doctor,
                                description=description)
