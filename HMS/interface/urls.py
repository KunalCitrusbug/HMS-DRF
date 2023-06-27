"""
URL configuration for HMS project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # user
    path('api/v0/user/', include("HMS.interface.user.urls")),
    path('api/v0/patient/', include("HMS.interface.patient.urls")),
    path('api/v0/doctor/', include("HMS.interface.doctor.urls")),
    path('api/v0/staff/', include("HMS.interface.staff.urls")),
    path('api/v0/medical-record/', include("HMS.interface.medical_record.urls")),

]
