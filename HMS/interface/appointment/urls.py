"""
This following file in the Django web framework that contains the URL patterns for your web application.
The file maps URLs to views, which are Python functions that handle the incoming HTTP requests
and generate the HTTP response.
"""

from django.urls import path

from HMS.interface.appointment.views import CreateAppointmentView, FetchAppointmentListView, UpdateAppointmentView, \
    AppointmentDeleteView

urlpatterns = [
    path('create/', CreateAppointmentView.as_view(), name="appointment-create"),
    path('fetch/', FetchAppointmentListView.as_view(), name="appointment-fetch"),
    path('update/<uuid:pk>/', UpdateAppointmentView.as_view(), name="appointment-update"),
    path('delete/<uuid:pk>/', AppointmentDeleteView.as_view(), name="appointment-delete")
]
