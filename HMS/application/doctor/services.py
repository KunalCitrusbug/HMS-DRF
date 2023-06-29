"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""
import json
from typing import Any, Dict, List

from django.db.models import QuerySet

from HMS.application.user.services import UserAppServices
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

    user_service = UserAppServices()

    def __init__(self):
        self.doctor_services = DoctorServices()

    def create_doctor_profile(self, doctor_data: Dict[str, Any], user_data: Dict[str, Any]) -> Doctor:
        """
        This method is responsible for creating a new Doctor profile based on the provided doctor data and user data.
        """
        user = self.user_service.create_user(data=user_data)
        try:
            doctor = self.doctor_services.get_doctor_factory().build_entity_with_id(
                user=user
            )
            doctor.save()
            if doctor_data.get("specialization"):
                specializations = json.loads(doctor_data.get("specialization"))
                for specialization in specializations:
                    doctor.specialization.add(specialization)
                return doctor
        except Exception as e:
            raise Exception("Error in Doctor service:{}".format(str(e)))

    def fetch_doctors_list(self) -> QuerySet:
        """
        This method is responsible for fetching a list of doctors from the database.
        """

        try:
            doctors = self.doctor_services.get_doctor_repo().all()
            return doctors
        except Exception as e:
            raise Exception("Error while fetching Doctor list:{}".format(str(e)))

    def doctor_details(self, doctor_id):
        """
        This method is responsible for fetching the details of a specific doctor based on the provided doctor_id.
        """
        try:
            doctor = self.doctor_services.get_doctor_by_id(id=doctor_id)
            return doctor
        except Exception as e:
            raise Exception("Error while fetching doctor's details:", e)
