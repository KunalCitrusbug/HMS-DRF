"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""

from rest_framework import serializers

from HMS.application.user.services import UserAppServices
from HMS.domain.user.models import User


class UserSerializer(serializers.ModelSerializer):
    user_service = UserAppServices()
    class Meta:
        model = User
        fields = ["id", "email", "password", "user_type"]

    def create(self, validated_data):
        create_user = self.user_service.create_user(data=validated_data)
        return create_user
