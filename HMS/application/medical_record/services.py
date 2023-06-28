"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""
import json
from typing import Dict, Any, List, Type
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import QuerySet

from HMS.application.user.services import UserAppServices
from HMS.domain.doctor.models import Doctor
from HMS.domain.doctor.services import DoctorServices
from HMS.domain.medical_records.models import MedicalRecord
from HMS.domain.medical_records.services import MedicalRecordServices
from HMS.domain.patient.models import Patient
from HMS.domain.patient.services import PatientServices
from HMS.domain.user.models import User
from HMS.interface.utils.exceptions import PatientNotExistsException, DoctorNotExistsException


class MedicalRecordAppService:
    """
    This module provides the application layer service for the Django domain-driven structure.
    It encapsulates the business logic and acts as an intermediary between the presentation layer
    (views) and the domain layer
    (models and repositories).
    """

    def __init__(self):
        self.medical_record_service = MedicalRecordServices()

    def create_medical_record(self, data: Dict[str, Any]) -> MedicalRecord:
        try:
            patient_obj = PatientServices().get_patient_repo().get(id=data.get("patient"))
        except PatientNotExistsException:
            raise PatientNotExistsException("Patient with given id not exists:")

        try:
            doctor_obj = DoctorServices().get_doctor_repo().get(id=data.get("doctor"))
        except DoctorNotExistsException:
            raise DoctorNotExistsException("Doctor with provided id not exists:")

        try:
            medical_record = self.medical_record_service.get_medical_record_factory().build_entity_with_id(
                patient=patient_obj,
                doctor=doctor_obj,
                description=data.get("description")
            )
            medical_record.save()
            return medical_record
        except IntegrityError as e:
            raise IntegrityError("Integrity Error occurred:", e)

    def fetch_medical_record_list(self) -> QuerySet:
        """
        This method is responsible for fetching a list of medical records from the database.
        """

        try:
            medical_records = self.medical_record_service.get_medical_record_repo().all()
            return medical_records
        except Exception as e:
            raise Exception("Error while fetching Patient list:{}".format(str(e)))

    def medical_record_details(self, medical_record_id) -> Type[MedicalRecord]:
        """
        This method is responsible for fetching the details of a specific medical record based on the provided
         medical_record_id.
        """
        try:
            medical_record = self.medical_record_service.get_medical_record_by_id(id=medical_record_id)
            return medical_record
        except Exception as e:
            raise Exception("Error while fetching Medical Record's details:", e)
