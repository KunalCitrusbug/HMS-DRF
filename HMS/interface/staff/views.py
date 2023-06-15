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
from HMS.interface.user.helper import create_user_helper


class StaffCreateView(APIView):
    staff_service = StaffAppServices()

    def post(self, request):
        try:
            with transaction.atomic():
                user = create_user_helper(data=request.data)
                user_obj = UserServices().get_user_by_id(user_id=user['id'])
                if user:
                    # Create a Staff Profile
                    serializer = StaffSerializer(data=request.data)
                    if serializer.is_valid():
                        staff = self.staff_service.create_staff_profile(data=request.data, user=user_obj)
                        return Response({"Success": 'Staff User Created', "id": staff.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
