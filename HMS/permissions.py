"""
This module defines custom permission classes used in Django REST Framework for controlling access to API views
and view-sets.
"""

from rest_framework.permissions import BasePermission

from HMS.application.patient.services import PatientAppServices
from HMS.domain.doctor.services import DoctorServices
from HMS.domain.patient.services import PatientServices
from HMS.domain.staff.services import StaffServices


class IsDoctorViewPermission(BasePermission):
    """
    This permission class determines whether a user has permission to access a view specifically designed for doctors.
    """

    def has_permission(self, request, view) -> bool:
        return request.user.user_type == 'Admin'


class IsDoctorSelf(BasePermission):
    """
    This permission class determines whether an authenticated user is a Doctor and also it cross-verify that
    doctor is accessing its own profile only.
    """

    doctor_service = DoctorServices()

    def has_permission(self, request, view, *args, **kwargs) -> bool:
        requested_uuid = request.__dict__.get('parser_context').get("kwargs").get("uuid")
        doctor_uuid = None
        if request.user.user_type == 'Doctor':
            doctor_uuid = self.doctor_service.get_doctor_repo().get(user=request.user)
            doctor_uuid = doctor_uuid.id
        return doctor_uuid == requested_uuid


class IsPatientViewPermission(BasePermission):
    """
    This permission class determines whether a user has permission to access a view specifically designed for patients.
    """

    def has_permission(self, request, view) -> bool:
        return request.user.user_type == 'Admin' or request.user.user_type == 'Doctor' or request.user.user_type == "Staff"


class IsAppointmentPermission(BasePermission):
    """
    This permission class determines whether a user has permission to access a view specifically designed for
    Appointments.
    """

    def has_permission(self, request, view) -> bool:
        return request.user.user_type == 'Admin' or request.user.user_type == 'Doctor' or request.user.user_type == "Staff"


class IsPatientSelf(BasePermission):
    """
    This permission class determines whether an authenticated user is a Patient and also it cross-verify that
    patient is accessing its own profile only.
    """

    patient_service = PatientServices()

    def has_permission(self, request, view, *args, **kwargs) -> bool:
        requested_uuid = request.__dict__.get('parser_context').get("kwargs").get("uuid")
        patient_uuid = None
        if request.user.user_type == 'Patient':
            patient_uuid = self.patient_service.get_patient_repo().get(user=request.user)
            patient_uuid = patient_uuid.id
        return patient_uuid == requested_uuid


class IsStaffViewPermission(BasePermission):
    """
    This permission class determines whether a user has permission to access a view specifically designed for staff.
    """

    def has_permission(self, request, view) -> bool:
        return request.user.user_type == 'Admin'


class IsStaffSelf(BasePermission):
    """
    This permission class determines whether an authenticated user is a Staff user and also it cross-verify that
    a staff user is accessing its own profile only.
    """
    staff_service = StaffServices()

    def has_permission(self, request, view, *args, **kwargs) -> bool:
        requested_uuid = request.__dict__.get('parser_context').get("kwargs").get("uuid")
        staff_uuid = None
        if request.user.user_type == 'Staff':
            staff_uuid = self.staff_service.get_staff_repo().get(user=request.user)
            staff_uuid = staff_uuid.id
        return staff_uuid == requested_uuid


class IsDoctorCreate(BasePermission):
    """
    This permission class determines whether an authenticated user is a Staff user and also it cross-verify that
    a staff user is accessing its own profile only.
    """

    def has_permission(self, request, view) -> bool:
        return request.user.user_type == 'Admin'


class IsStaffCreate(BasePermission):
    """
    This permission class determines whether an authenticated user is a Staff user and also it cross-verify that
    a staff user is accessing its own profile only.
    """

    def has_permission(self, request, view, *args, **kwargs) -> bool:
        return request.user.user_type == 'Admin' or request.user.user_type == 'Doctor'


class IsPatientCreate(BasePermission):
    """
    This permission class determines whether an authenticated user is a Staff user and also it cross-verify that
    a staff user is accessing its own profile only.
    """

    def has_permission(self, request, view, *args, **kwargs) -> bool:
        return request.user.user_type == 'Admin' or request.user.user_type == 'Doctor' or \
               request.user.user_type == 'Staff'
