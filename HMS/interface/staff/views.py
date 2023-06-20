"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from HMS.application.patient.services import PatientAppServices
from HMS.application.staff.services import StaffAppServices
from HMS.domain.user.services import UserServices
from HMS.interface.patient.serializers import PatientSerializer
from HMS.interface.staff.serializers import StaffSerializer
from HMS.interface.user.serializers import UserSerializer
from HMS.interface.utils import APIResponse


class StaffCreateView(APIView):
    staff_service = StaffAppServices()
    api_response = APIResponse()

    def post(self, request):
        pass
        try:
            with transaction.atomic():
                user_serializer = UserSerializer(data=request.data)
                staff_serializer = StaffSerializer(data=request.data)
                if user_serializer.is_valid() and staff_serializer.is_valid():
                    create_staff = self.staff_service.create_staff_profile(staff_data=staff_serializer.data,
                                                                           user_data=user_serializer.data)
                    if create_staff:
                        data = {'Name': create_staff.user.name, 'Contact': create_staff.user.contact_no,
                                'Gender': create_staff.user.gender, 'Staff Type': create_staff.staff_type}
                        return self.api_response.success(data=data, message="Patient Created Success")
                    else:
                        return self.api_response.fail(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                      errors={}, message="Failed to create staff user")
                else:
                    errors = {}
                    if not user_serializer.is_valid():
                        errors.update(user_serializer.errors)
                    if not staff_serializer.is_valid():
                        errors.update(staff_serializer.errors)
                    return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST, errors=errors,
                                                  message="Validation Error")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
