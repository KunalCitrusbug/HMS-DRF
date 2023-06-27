"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""

from rest_framework import serializers

from HMS.domain.doctor.models import Doctor
from HMS.domain.medical_records.models import MedicalRecord
from HMS.interface.specialization.serializers import SpecializationSerializer
from HMS.interface.user.serializers import UserListSerializer


class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances to JSON representation and vice versa.
    """

    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'description']
