"""
This following file contains all queries related to particular model.
"""

from typing import Type

from django.db.models.manager import BaseManager

from HMS.domain.appointment.models import AppointmentFactory, Appointment
from HMS.domain.patient.models import Patient, PatientFactory


class AppointmentServices:
    """
    This creates model service that provide abstract layer over
    a model, and user has to access the service layer instead of an accessing model.
    """

    def get_appointment_factory(
            self,
    ) -> Type[AppointmentFactory]:
        return AppointmentFactory

    def get_appointment_repo(self) -> BaseManager[Appointment]:
        return Appointment.objects

    @staticmethod
    def get_appointment_by_id(id: str) -> Type[Appointment]:
        return Appointment.objects.get(id=id)
