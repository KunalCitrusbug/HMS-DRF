"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from HMS.application.patient.services import PatientAppServices
from HMS.domain.user.services import UserServices
from HMS.interface.patient.serializers import PatientSerializer
from HMS.interface.user.helper import create_user_helper


class PatientCreateView(APIView):
    patient_service = PatientAppServices()

    def post(self, request):
        try:
            with transaction.atomic():
                user = create_user_helper(data=request.data)
                user_obj = UserServices().get_user_by_id(user_id=user['id'])
                if user:
                    # Create a Patient Profile
                    serializer = PatientSerializer(data=request.data)
                    if serializer.is_valid():
                        patient = self.patient_service.create_patient(data=request.data, user=user_obj)
                        return Response({"Success": 'Patient Created', "id": patient.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
