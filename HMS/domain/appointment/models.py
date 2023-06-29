"""
This file defines the structure of stored data,
including the field types and possibly related information
"""

import uuid
from dataclasses import dataclass
from datetime import datetime

from django.db import models

from HMS.domain.activity.models import Activity
from HMS.domain.doctor.models import Doctor
from HMS.domain.patient.models import Patient


@dataclass(frozen=True)
class AppointmentID:
    """
    This is a value object that should be used to generate and pass the
    PatientID to the Patient
    """

    value: uuid.UUID


class Appointment(Activity):
    """
    This following class is database structure of Medical Records of Patient.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        db_table = "appointment"

    def __str__(self):
        return f"Appointment ID: {self.id} - Patient: {self.patient} - Doctor: {self.doctor} - Date: {self.date} - Time: {self.time}"


class AppointmentFactory:
    """
    This following class is a Factory method of an above-mentioned model.
    """

    @staticmethod
    def build_entity(id: id, patient: Patient, doctor: Doctor,
                     date: datetime, time: datetime) -> Appointment:
        return Appointment(id=id, patient=patient, doctor=doctor, date=date, time=time)

    @classmethod
    def build_entity_with_id(cls, patient: Patient, doctor: Doctor,
                             date: datetime, time: datetime) -> Appointment:
        entity_id = AppointmentID(uuid.uuid4())
        return cls.build_entity(id=entity_id.value, patient=patient, doctor=doctor, date=date, time=time)
