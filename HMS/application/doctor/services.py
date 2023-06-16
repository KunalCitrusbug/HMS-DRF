"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""

from typing import Dict, Any

from HMS.domain.doctor.models import Doctor
from HMS.domain.doctor.services import DoctorServices
from HMS.domain.user.models import User


class DoctorAppServices:
    """
    This module provides the application layer service for the Django domain-driven structure.
    It encapsulates the business logic and acts as an intermediary between the presentation layer
    (views) and the domain layer
    (models and repositories).
    """


    def __init__(self):
        self.doctor_services = DoctorServices()

    def create_doctor_profile(self, data: Dict[str, Any], user: User) -> Doctor:
        try:

            doctor = self.doctor_services.get_doctor_factory().build_entity_with_id(
                specialization=data['specialization'], name=data['name'], doj=data['doj'],
                contact_no=data['contact_no'],
                user=user,
            )
            doctor.save()
            return doctor
        except Exception as e:
            raise Exception("Error in Doctor service:", e)
