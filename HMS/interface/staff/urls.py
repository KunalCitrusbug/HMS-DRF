"""
This following file in the Django web framework that contains the URL patterns for your web application.
The file maps URLs to views, which are Python functions that handle the incoming HTTP requests
and generate the HTTP response.
"""

from django.urls import path

from HMS.interface.staff.views import StaffCreateView, StaffListView, FetchStaffView

urlpatterns = [
    path('register/', StaffCreateView.as_view(), name="staffs-register"),
    path('staff-list/', StaffListView.as_view(), name="staffs-list"),
    path('fetch-staff/<uuid:uuid>/', FetchStaffView.as_view(), name="fetch-staff"),
]
