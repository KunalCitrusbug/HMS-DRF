"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""
from typing import Any, Dict

from django.db import transaction

from HMS.application.user.services import UserAppServices
from HMS.domain.patient.models import Patient
from HMS.domain.patient.services import PatientServices
from HMS.domain.user.models import User


class PatientAppServices:
    """
    This module provides the application layer service for the Django domain-driven structure.
    It encapsulates the business logic and acts as an intermediary between the presentation layer
    (views) and the domain layer
    (models and repositories).
    """

    user_service = UserAppServices()

    def __init__(self):
        self.patient_services = PatientServices()

    def create_patient(self, patient_data: Dict[str, Any], user_data: Dict[str, Any]) -> Patient:
        user = self.user_service.create_user(data=user_data)
        try:
            patient = self.patient_services.get_patient_factory().build_entity_with_id(
                age=patient_data['age'], dob=patient_data['dob'], address=patient_data['address'], user=user
            )
            patient.save()
            return patient
        except Exception as e:
            # Optionally, handle the exception or log the error
            raise ValueError("Error in Patient service: {}".format(str(e)))

