"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from HMS.application.doctor.services import DoctorAppServices
from HMS.domain.doctor.models import Doctor
from HMS.interface.doctor.serializers import DoctorSerializer
from HMS.interface.user.serializers import UserSerializer
from HMS.interface.utils import APIResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


class DoctorCreateView(APIView):
    doctor_service = DoctorAppServices()
    api_response = APIResponse()

    def post(self, request):
        pass
        try:
            with transaction.atomic():
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    create_doctor = self.doctor_service.create_doctor_profile(user_data=user_serializer.data,
                                                                              doctor_data=request.data)
                    if create_doctor:
                        data = {'Name': create_doctor.user.name, 'Contact': create_doctor.user.contact_no,
                                'Gender': create_doctor.user.gender}
                        return self.api_response.success(data=data, message="Patient Created Success")
                    else:
                        return self.api_response.fail(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                      errors={}, message="Failed to create Doctor")
                else:
                    errors = {}
                    if not user_serializer.is_valid():
                        errors.update(user_serializer.errors)
                    return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST, errors=errors,
                                                  message="Validation Error")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FetchDoctor(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    api_response = APIResponse()

    def get(self, request):
        doctors = Doctor.objects.all()
        data = {}
        for obj in doctors:
            import pdb;pdb.set_trace()

            data[obj]['Name'] = obj.user.name
            data[obj]['Contact'] = obj.user.contact_no
            data[obj]['Gender'] = obj.user.gender
            data[obj]['Name'] = obj.user.name
        return self.api_response.success(message="Doctor", data=data)
