"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from HMS.application.patient.services import PatientAppServices
from HMS.domain.user.services import UserServices
from HMS.interface.patient.serializers import PatientSerializer
from HMS.interface.user.serializers import UserSerializer
from HMS.interface.utils import APIResponse


class PatientCreateView(APIView):
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
