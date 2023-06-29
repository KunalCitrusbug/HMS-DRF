"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""
from typing import Any, Dict, Type

from django.db.models import QuerySet

from HMS.application.user.services import UserAppServices
from HMS.domain.staff.models import Staff
from HMS.domain.staff.services import StaffServices


class StaffAppServices:
    """
    This module provides the application layer service for the Django domain-driven structure.
    It encapsulates the business logic and acts as an intermediary between the presentation layer
    (views) and the domain layer
    (models and repositories).
    """

    user_service = UserAppServices()

    def __init__(self):
        self.staff_services = StaffServices()

    def create_staff_profile(self, staff_data: Dict[str, Any], user_data: Dict[str, Any]) -> Staff:
        user = self.user_service.create_user(data=user_data)
        try:
            staff = self.staff_services.get_staff_factory().build_entity_with_id(staff_type=staff_data['staff_type'],
                                                                                 user=user)
            staff.save()
            return staff
        except Exception as e:
            raise Exception("Error in Staff service:{}".format(str(e)))

    def fetch_staff_list(self) -> QuerySet:
        """
        This method is responsible for fetching a list of staff from the database.
        """

        try:
            staff = self.staff_services.get_staff_repo().all()
            return staff
        except Exception as e:
            raise Exception("Error while fetching Staff list:{}".format(str(e)))

    def staff_details(self, staff_id) -> Type[Staff]:
        """
        This method is responsible for fetching the details of a specific staff based on the provided staff_id.
        """
        try:
            staff = self.staff_services.get_staff_by_id(id=staff_id)
            return staff
        except Exception as e:
            raise Exception("Error while fetching staff's details:", e)
