"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from HMS.application.medical_record.services import MedicalRecordAppService
from HMS.interface.medical_record.serializers import MedicalRecordCreateSerializer
from HMS.interface.utils.api_response import APIResponse
from HMS.interface.utils.exceptions import PatientNotExistsException, DoctorNotExistsException
from HMS.permissions import IsPatientCreate, IsPatientViewPermission


class MedicalRecordCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsPatientCreate]
    medical_record_app_service = MedicalRecordAppService()
    api_response = APIResponse()

    def post(self, request):
        try:
            medical_record_obj = self.medical_record_app_service.create_medical_record(data=request.data)
            medical_record_serializer = MedicalRecordCreateSerializer(medical_record_obj)
            return self.api_response.success(message="Medical Record Created", data=medical_record_serializer.data,
                                             status=status.HTTP_201_CREATED)
        except PatientNotExistsException as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Patient does not exists: " + str(e))

        except DoctorNotExistsException as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Doctor does not exists: " + str(e))

        except IntegrityError as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Profile already exists: " + str(e))
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to Create medical record: " + str(e))


class MedicalRecordsListView(APIView):
    """
    This class represents an API view for fetching a list of patients.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsPatientViewPermission]
    api_response = APIResponse()
    medical_record_app_service = MedicalRecordAppService()

    def get(self, request):
        try:
            medical_records = self.medical_record_app_service.fetch_medical_record_list()
            data = MedicalRecordCreateSerializer(medical_records, many=True)
            return self.api_response.success(message="Medical Records", data=data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to fetch medical records: " + str(e))
