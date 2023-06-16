"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from HMS.application.doctor.services import DoctorAppServices
from HMS.domain.user.services import UserServices
from HMS.interface.doctor.serializers import DoctorSerializer


class DoctorCreateView(APIView):
    doctor_service = DoctorAppServices()

    def post(self, request):
        pass
    #     try:
    #         with transaction.atomic():
    #             user = create_user_helper(data=request.data)
    #             user_obj = UserServices().get_user_by_id(user_id=user['id'])
    #             if user:
    #                 # Create a Patient Profile
    #                 serializer = DoctorSerializer(data=request.data)
    #                 if serializer.is_valid():
    #                     doctor = self.doctor_service.create_doctor_profile(data=request.data, user=user_obj)
    #                     return Response({"Success": 'Doctor Created', "id": doctor.id},
    #                                     status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
