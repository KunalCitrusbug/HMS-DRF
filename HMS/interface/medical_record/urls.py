"""
This following file in the Django web framework that contains the URL patterns for your web application.
The file maps URLs to views, which are Python functions that handle the incoming HTTP requests
and generate the HTTP response.
"""

from django.urls import path

from HMS.interface.medical_record.views import MedicalRecordCreateView, MedicalRecordsListView, MedicalRecordDetailView, \
    MedicalRecordDeleteView

urlpatterns = [
    path('create/', MedicalRecordCreateView.as_view(), name="medical-record-create"),
    path('list/', MedicalRecordsListView.as_view(), name="medical-record-list"),
    path('medical-record/<uuid:pk>/', MedicalRecordDetailView.as_view(), name="medical-record-list"),
    path('medical-record-delete/<uuid:pk>/', MedicalRecordDeleteView.as_view(), name="medical-record-delete")
]
