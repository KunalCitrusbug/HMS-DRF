"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""

import json
from typing import Any, Dict

from django.db import transaction
from django.db.models import QuerySet

from HMS.application.doctor.services import DoctorAppServices
from HMS.application.patient.services import PatientAppServices
from HMS.domain.appointment.models import Appointment
from HMS.domain.appointment.services import AppointmentServices
from HMS.interface.utils.exceptions import DoctorNotAvaliableException


class AppointmentAppService:
    """
    This module provides the application layer service for the Django domain-driven structure.
    It encapsulates the business logic and acts as an intermediary between the presentation layer
    (views) and the domain layer
    (models and repositories).
    """

    def __init__(self):
        self.appointment_service = AppointmentServices()

    def create_appointment(self, data: Dict[str, Any]) -> Appointment:
        """
        Create a new appointment.
        """
        try:
            with transaction.atomic():
                # Get a patient object
                patient_obj = PatientAppServices().patient_details(patient_id=data.get('patient'))
                # Get a doctor object
                doctor_obj = DoctorAppServices().doctor_details(doctor_id=data.get('doctor'))
                date = data.get('date')
                time = data.get('time')
                is_available = is_doctor_available(doctor_obj, date, time)
                if is_available:

                    appointment = self.appointment_service.get_appointment_factory().build_entity_with_id(
                        patient=patient_obj, doctor=doctor_obj, date=date, time=time
                    )
                    appointment.save()
                    return appointment
                else:
                    # Handle doctor not available error
                    raise DoctorNotAvaliableException('Doctor is not available at the specified date and time')
        except Exception as e:
            # Handle any other exceptions that may occur during appointment creation
            raise Exception(f'Error creating appointment: {str(e)}')

    def fetch_all_appointments(self):
        """
        Fetch all appointments.
        """
        try:
            appointments = self.appointment_service.get_appointment_repo().all()
            return appointments
        except Exception as e:
            raise Exception("Error while fetching appointments:", e)

    def fetch_appointment(self, params: QuerySet) -> QuerySet:
        """
        Fetch appointments based on query parameters.
        """
        try:
            queryset = self.appointment_service.get_appointment_repo().all()
            patient_id = params.get('patient_id')
            doctor_id = params.get('doctor_id')

            if patient_id and doctor_id:
                raise ValueError("Only one of 'patient_id' or 'doctor_id' should be provided, not both.")

            if patient_id:
                patient_obj = PatientAppServices().patient_details(patient_id=patient_id)
                queryset = queryset.filter(patient=patient_obj)

            if doctor_id:
                doctor_obj = DoctorAppServices().doctor_details(doctor_id=doctor_id)
                queryset = queryset.filter(doctor=doctor_obj)

            is_completed = params.get('is_completed')
            if is_completed:
                queryset = queryset.filter(is_completed=is_completed)

            date = params.get('date')
            if date:
                queryset = queryset.filter(date=date)

            return queryset

        except ValueError as ve:
            raise ValueError(f"Invalid input parameters: {ve}")

        except Exception as e:
            raise Exception("An unexpected error occurred while fetching appointments")


def is_doctor_available(doctor, date, time):
    """
    Check if the doctor is available at the specified date and time.
    """

    appointment = AppointmentServices().get_appointment_repo().filter(doctor=doctor, date=date, time=time)
    return not appointment.exists()
