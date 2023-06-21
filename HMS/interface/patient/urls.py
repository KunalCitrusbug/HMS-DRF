"""
This following file in the Django web framework that contains the URL patterns for your web application.
The file maps URLs to views, which are Python functions that handle the incoming HTTP requests
and generate the HTTP response.
"""

from django.urls import path

from HMS.interface.patient.views import PatientCreateView, PatientListView, FetchPatientView

urlpatterns = [
    path('register/', PatientCreateView.as_view(), name="patient-register"),
    path('patient-list/', PatientListView.as_view(), name="patient-list"),
    path('patient/<uuid:uuid>/', FetchPatientView.as_view(), name="patient"),
]
