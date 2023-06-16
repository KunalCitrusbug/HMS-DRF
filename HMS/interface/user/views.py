"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from ..utils import APIResponse


class RegisterView(APIView):
    """
    This view class handles the registration of a new user.
    """

    api_response = APIResponse()

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid()
            serializer.save()
            return self.api_response.success(data=serializer.data, message="User Created Success")
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
