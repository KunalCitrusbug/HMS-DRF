from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError


class InvalidPasswordException(ValidationError):
    pass


class PatientNotExistsException(ObjectDoesNotExist):
    pass

class DoctorNotExistsException(ObjectDoesNotExist):
    pass
