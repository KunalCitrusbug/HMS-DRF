"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from HMS.application.staff.services import StaffAppServices
from HMS.interface.staff.serializers import StaffSerializer, StaffListSerializer
from HMS.interface.user.serializers import UserSerializer
from HMS.interface.utils.api_response import APIResponse
from HMS.permissions import IsStaffViewPermission, IsStaffSelf, IsStaffCreate


class StaffCreateView(APIView):
    """
    This class represents an API view for creating a staff profile.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsStaffCreate]
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


class StaffListView(APIView):
    """
    This class represents an API view for fetching a list of staff members.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsStaffViewPermission]
    staff_service = StaffAppServices()
    api_response = APIResponse()

    def get(self, request):
        try:
            staff = self.staff_service.fetch_staff_list()
            data = StaffListSerializer(staff, many=True)
            return self.api_response.success(message="Staff List", data=data.data)
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to fetch Staff list: " + str(e))


class StaffDetailView(APIView):
    """
    This class represents an API view for fetching and updating details of a staff member.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsStaffViewPermission | IsStaffSelf]
    staff_service = StaffAppServices()
    api_response = APIResponse()

    def get(self, request, *args, **kwargs):
        try:
            staff = self.staff_service.staff_details(staff_id=self.kwargs.get("uuid"))
            serialized_data = StaffListSerializer(staff)
            return self.api_response.success(message="Staff's Details", data=serialized_data.data)

        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to fetch staff's details: " + str(e))

    def patch(self, request, *args, **kwargs):
        try:
            staff = self.patient_service.patient_details(patient_id=self.kwargs.get("uuid"))
            user_obj = patient_obj.user
            patient_serializer = PatientUpdateSerializer(patient_obj, data=request.data, partial=True)
            user_serializer = UserUpdateSerializer(user_obj, data=request.data, partial=True)
            if patient_serializer.is_valid() and user_serializer.is_valid():
                user_serializer.save()
                patient_serializer.save()
                serialized_data = PatientListSerializer(patient_obj)
                return self.api_response.success(message="Patient's Details Updated", data=serialized_data.data)
            else:
                errors = {}
                if not patient_serializer.is_valid():
                    errors.update(patient_serializer.errors)
                if not user_serializer.is_valid():
                    errors.update(user_serializer.errors)

                return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST, errors=errors,
                                              message="Validation Error")
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to update patient: " + str(e))

