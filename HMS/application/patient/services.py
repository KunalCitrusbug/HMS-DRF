"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""
from HMS.domain.patient.services import PatientServices
from HMS.domain.user.services import UserServices


class PatientAppServices:
    def __init__(self):
        self.patient_services = PatientServices()

    def create_patient(self, data, user):
        try:
            patient = self.patient_services.get_patient_factory().build_entity_with_id(
                name=data['name'], dob=data['dob'], gender=data['gender'], contact_no=data['contact_no'],
                address=data['address'], user=user
            )
            patient.save()
            return patient
        except Exception as e:
            raise Exception("Error in Patient service:", e)
