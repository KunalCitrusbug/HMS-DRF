"""
This is a view module to define list, create, update, delete views.
You can define different view properties here.
"""

from datetime import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...domain.patient.services import PatientServices
from .helper import create_user_helper
from .serializers import UserSerializer


# view for registering users
class RegisterView(APIView):
    def post(self, request):
        try:
            user = create_user_helper(data=request.data)
            return Response({"Success": 'User Created', "id": user['id']}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
