"""
This following is a Helper file that basically contains such functions that
help in API calls
"""
from rest_framework.exceptions import ValidationError

from HMS.interface.user.serializers import UserSerializer


def create_user_helper(data):
    try:
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        return serializer.data
    except Exception as e:
        raise Exception("Error while creating user:", e)

