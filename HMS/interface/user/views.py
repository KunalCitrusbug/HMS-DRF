"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""

from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from ..utils.api_response import APIResponse
from ...application.user.services import UserAppServices


class RegisterView(APIView):
    """
    This view class handles the registration of a new user.
    """

    api_response = APIResponse()
    user_service = UserAppServices()

    def post(self, request):
        try:
            with transaction.atomic():
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    create_user = self.user_service.create_user(data=serializer.data)
                    if create_user:
                        data = {'email': create_user.email, 'name': create_user.name,
                                'contact_no': create_user.contact_no,
                                'gender': create_user.gender}
                        return self.api_response.success(data=data, message="User Created Success",
                                                         status=status.HTTP_201_CREATED)
                    else:
                        # Handle the case when the user is not created
                        return self.api_response.fail(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                      errors={}, message="Failed to create user")
                else:
                    return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST, errors=serializer.errors,
                                                  message="Validation Error")

        except ValidationError as e:
            # Handle validation errors
            errors = e.get_full_details()  # Get detailed error messages
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST, errors=errors, message="Validation Error")
        except Exception as e:
            # Handle other exceptions
            import traceback
            traceback.print_exc()  # Print traceback for debugging purposes
            return self.api_response.fail(status=status.HTTP_500_INTERNAL_SERVER_ERROR, errors={}, message="Server "
                                                                                                           "Error")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Customize the response data here
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    api_response = APIResponse()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_pair = serializer.validated_data

        data = {
            'access_token': token_pair['access'],
            'refresh_token': token_pair['refresh'],
        }

        # Access the api_response from the serializer class
        return self.api_response.success(data=data, message="Login succeed", status=200)
