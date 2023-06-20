"""
This following file in the Django web framework that contains the URL patterns for your web application.
The file maps URLs to views, which are Python functions that handle the incoming HTTP requests
and generate the HTTP response.
"""

from django.urls import path

from HMS.interface.doctor.views import DoctorCreateView, FetchDoctor

urlpatterns = [
    path('register/', DoctorCreateView.as_view(), name="doctor-register"),
    path('doctor-list/', FetchDoctor.as_view(), name="doctor-list"),
]
