"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""

from rest_framework import serializers

from HMS.domain.staff.models import Staff
from HMS.interface.user.serializers import UserListSerializer


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["staff_type"]


class StaffListSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances for a Staff list
    """

    user = UserListSerializer()

    class Meta:
        model = Staff
        fields = ['id', 'user', 'staff_type']
