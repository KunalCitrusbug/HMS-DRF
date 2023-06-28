"""
This is a view module to define a list, create, update, delete views.
You can define different view properties here.
"""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from HMS.application.appointment.services import AppointmentAppService
from HMS.interface.appointment.serializers import AppointmentListSerializer, AppointmentUpdateSerializer
from HMS.interface.utils.api_response import APIResponse
from HMS.interface.utils.exceptions import DoctorNotAvaliableException
from HMS.permissions import IsAppointmentPermission


class CreateAppointmentView(APIView):
    appointment_service = AppointmentAppService()
    api_response = APIResponse()
    permission_classes = [IsAuthenticated & IsAppointmentPermission]

    def post(self, request):
        try:
            serializer = AppointmentListSerializer(data=request.data)
            serializer.is_valid()
            appointment = self.appointment_service.create_appointment(data=serializer.data)
            serialized_data = AppointmentListSerializer(appointment)
            return self.api_response.success(message="Appointment Created", data=serialized_data.data,
                                             status=status.HTTP_201_CREATED)
        except DoctorNotAvaliableException as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Doctor Not available: " + str(e))

        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Failed to create appointment: " + str(e))


class FetchAppointmentListView(APIView):
    serializer_class = AppointmentListSerializer
    appointment_service = AppointmentAppService()
    api_response = APIResponse()
    queryset = appointment_service.fetch_all_appointments()
    update_serializer_class = AppointmentUpdateSerializer

    def get(self, request, *args, **kwargs):
        try:
            params = self.request.query_params
            appointment = self.appointment_service.fetch_appointment(params=params)
            serialized_data = AppointmentListSerializer(appointment, many=True)
            return self.api_response.success(message="Appointment", data=serialized_data.data,
                                             status=status.HTTP_200_OK)
        except ValueError as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="value error: " + str(e))

        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Error in fetching appointments: " + str(e))


class UpdateAppointmentView(RetrieveUpdateAPIView):
    appointment_service = AppointmentAppService()
    api_response = APIResponse()
    queryset = appointment_service.fetch_all_appointments()
    serializer_class = AppointmentUpdateSerializer

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.api_response.success(message="Appointment Updated", data=serializer.data,
                                                 status=status.HTTP_200_OK)
            else:
                return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                              errors={},
                                              message="Failed to update appointment: " + str(serializer.errors))
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Error in updating appointment: " + str(e))


class AppointmentDeleteView(DestroyAPIView):
    appointment_service = AppointmentAppService()
    api_response = APIResponse()
    queryset = appointment_service.fetch_all_appointments()

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return self.api_response.success(message="Appointment Deleted", data={},
                                             status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Object not exists")
        except Exception as e:
            return self.api_response.fail(status=status.HTTP_400_BAD_REQUEST,
                                          errors={}, message="Error in delete appointment: " + str(e))
