"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""

from rest_framework import serializers

from HMS.domain.specialization.models import Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances to JSON representation and vice versa.
    """

    class Meta:
        model = Specialization
        fields = ['id', 'title']
