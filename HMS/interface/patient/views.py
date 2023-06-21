"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from HMS.application.patient.services import PatientAppServices
from HMS.domain.user.services import UserServices
from HMS.interface.patient.serializers import PatientSerializer, PatientListSerializer, PatientUpdateSerializer
from HMS.interface.user.serializers import UserSerializer, UserUpdateSerializer
from HMS.interface.utils import APIResponse
from HMS.permissions import IsPatientViewPermission, IsPatientSelf


class PatientCreateView(APIView):
    """
    This class represents an API view for creating a new patient.
    """

    patient_service = PatientAppServices()
    api_response = APIResponse()

    def post(self, request):
        try:
            with transaction.atomic():
                user_serializer = UserSerializer(data=request.data)
                patient_serializer = PatientSerializer(data=request.data)
                if user_serializer.is_valid() and patient_serializer.is_valid():
                    # Both user and patient serializers are valid, continue processing
                    create_patient = self.patient_service.create_patient(patient_data=patient_serializer.data,
                                                                         user_data=user_serializer.data)
                    if create_patient:
                        data = {'Name': create_patient.user.name, 'Contact': create_patient.user.contact_no,
                                'Gender': create_patient.user.gender, 'Age': create_patient.age,
                                'DOB': create_patient.dob, 'Address': create_patient.address}
                        return self.api_response.success(data=data, message="Patient Created Success")
                    else:
                        return self.api_response.fail(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                      errors={}, message="Failed to create patient")
                else:
                    # At least one serializer is invalid, return a validation error response
                    errors = {}
                    if not user_serializer.is_valid():
                        errors.update(user_serializer.errors)
                    if not patient_serializer.is_valid():
                        errors.update(patient_serializer.errors)

                    return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST, errors=errors,
                                                  message="Validation Error")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PatientListView(APIView):
    """
    This class represents an API view for fetching a list of patients.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsPatientViewPermission]
    patient_service = PatientAppServices()
    api_response = APIResponse()

    def get(self, request):
        try:
            patient = self.patient_service.fetch_patients_list()
            data = PatientListSerializer(patient, many=True)
            return self.api_response.success(message="Patients List", data=data.data)
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to fetch patients list: " + str(e))


class FetchPatientView(APIView):
    """
    This class represents an API view for fetching and updating the details of a patient.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsPatientViewPermission | IsPatientSelf]
    patient_service = PatientAppServices()
    api_response = APIResponse()

    def get(self, request, *args, **kwargs):
        try:
            patient = self.patient_service.patient_details(patient_id=self.kwargs.get("uuid"))
            serialized_data = PatientListSerializer(patient)
            return self.api_response.success(message="Patient's Details", data=serialized_data.data)

        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to fetch patient's details: " + str(e))

    def patch(self, request, *args, **kwargs):
        patient_obj = self.patient_service.patient_details(patient_id=self.kwargs.get("uuid"))
        user_obj = patient_obj.user
        patient_serializer = PatientUpdateSerializer(patient_obj, data=request.data, partial=True)
        user_serializer = UserUpdateSerializer(user_obj, data=request.data, partial=True)
        if patient_serializer.is_valid() and user_serializer.is_valid():
            user_serializer.save()
            patient_serializer.save()
            serialized_data = PatientListSerializer(patient_obj)
            return self.api_response.success(message="Patient's Details", data=serialized_data.data)
        else:
            errors = {}
            if not patient_serializer.is_valid():
                errors.update(patient_serializer.errors)
            if not user_serializer.is_valid():
                errors.update(user_serializer.errors)

            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST, errors=errors,
                                          message="Validation Error")
