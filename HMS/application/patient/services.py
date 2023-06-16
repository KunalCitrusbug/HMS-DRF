"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""
from typing import Any, Dict

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

    def __init__(self):
        self.patient_services = PatientServices()

    def create_patient(self, patient_data: Dict[str, Any], user_data: Dict[str, Any]) -> Patient:
        try:
            patient = self.patient_services.get_patient_factory().build_entity_with_id(
                age=data['age'], dob=data['dob'], address=data['address'], user=user
            )
            patient.save()
            return patient
        except Exception as e:
            raise Exception("Error in Patient service:", e)
