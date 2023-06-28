"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""

from rest_framework import serializers

from HMS.domain.appointment.models import Appointment


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances to JSON representation and vice versa.
    """

    class Meta:
        model = Appointment
        fields = ('patient', 'doctor', 'date', 'time')


class AppointmentListSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances to JSON representation and vice versa.
    """

    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances to JSON representation and vice versa.
    """

    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'time')
