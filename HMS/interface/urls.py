"""
URL configuration for HMS project.
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="HMS - DRF",
        default_version='v1',
        description="Hospital Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # user
    path('api/v0/user/', include("HMS.interface.user.urls")),
    path('api/v0/patient/', include("HMS.interface.patient.urls")),
    path('api/v0/doctor/', include("HMS.interface.doctor.urls")),
    path('api/v0/staff/', include("HMS.interface.staff.urls")),
    path('api/v0/medical-record/', include("HMS.interface.medical_record.urls")),
    path('api/v0/appointment/', include("HMS.interface.appointment.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
