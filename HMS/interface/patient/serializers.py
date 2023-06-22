"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""

from rest_framework import serializers

from HMS.application.user.services import UserAppServices
from HMS.domain.patient.models import Patient
from HMS.interface.user.serializers import UserListSerializer


class PatientSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances to JSON representation and vice versa.
    """

    patient_service = UserAppServices()

    class Meta:
        model = Patient
        fields = ["age", "dob", "address"]


class PatientListSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances for a Patient list
    """

    user = UserListSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'age', 'dob', 'address']


class PatientUpdateSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances for a Patient Update
    """

    class Meta:
        model = Patient
        fields = ['age', 'dob', 'address']
