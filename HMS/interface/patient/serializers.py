"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""

from rest_framework import serializers

from HMS.application.user.services import UserAppServices
from HMS.domain.patient.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    patient_service = UserAppServices()

    class Meta:
        model = Patient
        fields = ["id", "name", "dob", "gender", "contact_no", "address"]
