"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from HMS.application.medical_record.services import MedicalRecordAppService
from HMS.domain.medical_records.models import MedicalRecord
from HMS.interface.medical_record.serializers import MedicalRecordCreateSerializer, MedicalRecordUpdateSerializer, \
    MedicalRecordListSerializer
from HMS.interface.utils.api_response import APIResponse
from HMS.interface.utils.exceptions import PatientNotExistsException, DoctorNotExistsException
from HMS.permissions import IsPatientCreate, IsPatientViewPermission, IsPatientSelf


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
            data = MedicalRecordListSerializer(medical_records, many=True)
            return self.api_response.success(message="Medical Records", data=data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to fetch medical records: " + str(e))


class MedicalRecordDetailView(RetrieveUpdateAPIView):
    """
    This class represents an API view for fetching and updating the details of a medical record.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsPatientViewPermission | IsPatientSelf]
    medical_record_app_service = MedicalRecordAppService()
    api_response = APIResponse()
    queryset = medical_record_app_service.fetch_medical_record_list()
    serializer_class = MedicalRecordUpdateSerializer

    def get(self, request, *args, **kwargs):
        try:
            medical_record = self.medical_record_app_service.medical_record_details(
                medical_record_id=self.kwargs.get("pk"))
            data = MedicalRecordListSerializer(medical_record)
            return self.api_response.success(message="Medical Record's Details", data=data.data,
                                             status=status.HTTP_200_OK)

        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to fetch medical record's details: " + str(e))

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.api_response.success(message="Medical Record Updated", data=serializer.data,
                                                 status=status.HTTP_200_OK)
            else:
                return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                              errors={}, message="Failed to update medical record's details: " + str(
                        serializer.errors))
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Error in update medical record's details: " + str(e))


class MedicalRecordDeleteView(DestroyAPIView):
    medical_record_app_service = MedicalRecordAppService()
    queryset = medical_record_app_service.fetch_medical_record_list()
    api_response = APIResponse()
    permission_classes = [IsAuthenticated & IsPatientViewPermission | IsPatientSelf]

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return self.api_response.success(message="Medical Record Deleted", data={},
                                             status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Object not exists")
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Error in delete medical record's details: " + str(e))
