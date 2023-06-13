"""
URL configuration for HMS project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # user
    path('api/v0/user/', include("HMS.interface.user.urls")),

]
