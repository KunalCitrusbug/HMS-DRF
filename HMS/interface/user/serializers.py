"""
This following file is responsible for converting complex data types, such as Django model instances,
into a format suitable for rendering in API responses or for parsing in request data.
"""

from rest_framework import serializers

from HMS.domain.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "user_type"]

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], user_type=validated_data['user_type'])
        user.set_password(validated_data['password'])
        user.save()
        return user
