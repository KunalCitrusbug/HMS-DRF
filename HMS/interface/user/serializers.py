"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""

from rest_framework import serializers
from typing import Dict, Any
from HMS.application.user.services import UserAppServices
from HMS.domain.user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances to JSON representation and vice versa.
    """
    user_service = UserAppServices()

    class Meta:
        model = User
        fields = ["email", "password", "name", "contact_no", "gender"]


def create(self, validated_data: Dict[str, Any]) -> User:
    """
    This method is responsible for creating a new User object based on the validated data provided by
    accessing the application layer.
    """

    create_user = self.user_service.create_user(data=validated_data)
    return create_user
