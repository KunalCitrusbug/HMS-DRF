"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""
from typing import Any, Dict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from HMS.domain.user.models import User
from HMS.interface.utils.password_validator import password_validator


class UserSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances to JSON representation and vice versa.
    """

    class Meta:
        model = User
        fields = ["email", "password", "name", "contact_no", "gender", "user_type"]


def create(self, validated_data: Dict[str, Any]) -> User:
    """
    This method is responsible for creating a new User object based on the validated data provided by
    accessing the application layer.
    """

    create_user = self.user_service.create_user(data=validated_data)
    return create_user


class UserListSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances for User's list.
    """

    class Meta:
        model = User
        fields = ["email", "name", "contact_no", "gender"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to convert model instances for updating user.
    """

    class Meta:
        model = User
        fields = ["name", "contact_no", "gender"]
