"""
This following file in the Django web framework that contains the URL patterns for your web application.
The file maps URLs to views, which are Python functions that handle the incoming HTTP requests
and generate the HTTP response.
"""

from django.urls import path
from rest_framework import routers

from HMS.interface.user.views import RegisterView

# annotation_pattern = r"annotation"
#
# router = routers.SimpleRouter()
# router.register(r'signup', RegisterView, basename='user-signup')

urlpatterns = [
    path('signup/', RegisterView.as_view(), name="sign_up"),
]
