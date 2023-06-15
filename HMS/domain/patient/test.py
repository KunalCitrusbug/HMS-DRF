"""
This following file is document, which has a set of
    Test data,
    Pre-Conditions,
    Expected results,
    Post-Conditions
developed for a particular module and for code coverage
"""

from django.db.models.query import QuerySet
from django.test import TestCase

from HMS.domain.patient.models import PatientFactory, Patient
from HMS.domain.patient.services import PatientServices



class TestPatient(TestCase):
    """
    This following file contains test-cases
    to check code functionality and code coverage.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.patient_factory = PatientFactory()
        cls.patient_service = PatientServices()
        return super().setUpClass()

    def test_get_factory_method(self):
        try:
            self.patient_factory.build_entity
            self.patient_factory.build_entity_with_id
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Unexpected failure: {e}")

    def test_get_patient_repo_returns_expected_object_type(self):
        repo = self.patient_service.get_patient_repo()
        objects = repo.all()
        self.assertEqual(type(objects), QuerySet)
        self.assertEqual(objects.model, Patient)

    def test_plan_with_build_entity_with_id(self):
        try:
            email = "test@gmail.com"
            password = "test@1234"
            user_type = "Patient"  # user-type(s) : Admin/Staff/Doctor/Patient
            user_obj = self.user_service.get_user_factory().build_entity_with_id(
                email=email,
                is_admin=False,
                is_active=True,
                password=password,
                user_type=user_type  # user-type(s) : Admin/Staff/Doctor/Patient
            )
            self.assertEqual(user_obj.email, email)
            self.assertEqual(user_obj.user_type, user_type)
        except Exception as e:
            self.fail(f"Unexpected failure: {e}")
