"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""

import json

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from HMS.application.doctor.services import DoctorAppServices
from HMS.interface.doctor.serializers import DoctorListSerializer, DoctorUpdateSerializer
from HMS.interface.user.serializers import UserSerializer, UserUpdateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from HMS.interface.utils.api_response import APIResponse
from HMS.permissions import IsDoctorViewPermission, IsDoctorSelf, IsDoctorCreate


class DoctorCreateView(APIView):
    """
    This class represents an API view for creating a doctor's profile.
    """
    doctor_service = DoctorAppServices()
    api_response = APIResponse()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsDoctorCreate]

    def post(self, request):
        try:
            with transaction.atomic():
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    create_doctor = self.doctor_service.create_doctor_profile(user_data=user_serializer.data,
                                                                              doctor_data=request.data)
                    if create_doctor:
                        data = {'Name': create_doctor.user.name, 'Contact': create_doctor.user.contact_no,
                                'Gender': create_doctor.user.gender}
                        return self.api_response.success(data=data, message="Doctor Created Success",
                                                         status=status.HTTP_201_CREATED)
                    else:
                        return self.api_response.fail(status=status.HTTP_400_INTERNAL_SERVER_ERROR,
                                                      errors={}, message="Failed to create Doctor")
                else:
                    errors = {}
                    if not user_serializer.is_valid():
                        errors.update(user_serializer.errors)
                    return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST, errors=errors,
                                                  message="Validation Error")
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to create doctor: " + str(e))


class DoctorListView(APIView):
    """
    This class represents an API view for fetching a list of doctors.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsDoctorViewPermission]
    api_response = APIResponse()
    doctor_service = DoctorAppServices()

    def get(self, request):
        try:
            doctors = self.doctor_service.fetch_doctors_list()
            data = DoctorListSerializer(doctors, many=True)
            return self.api_response.success(message="Doctor", data=data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to fetch doctors list: " + str(e))


class DoctorDetailView(APIView):
    """
    This class represents an API view for fetching and updating doctor details.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsDoctorViewPermission | IsDoctorSelf]
    api_response = APIResponse()
    doctor_service = DoctorAppServices()

    def get(self, request, *args, **kwargs):
        # Fetch Doctor's Details
        try:
            doctor = self.doctor_service.doctor_details(doctor_id=self.kwargs.get("uuid"))
            serialized_data = DoctorListSerializer(doctor)

            return self.api_response.success(message="Doctor", data=serialized_data.data, status=status.HTTP_200_OK)

        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to fetch doctor's details: " + str(e))

    def patch(self, request, *args, **kwargs):
        try:
            doctor_obj = self.doctor_service.doctor_details(doctor_id=self.kwargs.get("uuid"))
            user_obj = doctor_obj.user
            user_serializer = UserUpdateSerializer(user_obj, data=request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
                specializations = json.loads(request.data.get("specialization"))
                for specialization in specializations:
                    doctor_obj.specialization.clear()
                    doctor_obj.specialization.add(specialization)
                serialized_data = DoctorListSerializer(doctor_obj)
                return self.api_response.success(message="Doctor's Details Updated", data=serialized_data.data,
                                                 status=status.HTTP_200_OK)
            else:
                errors = {}
                if not user_serializer.is_valid():
                    errors.update(user_serializer.errors)

                return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST, errors=errors,
                                              message="Validation Error")
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to update doctor: " + str(e))
