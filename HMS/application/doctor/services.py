"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""
from HMS.domain.doctor.services import DoctorServices


class DoctorAppServices:
    def __init__(self):
        self.doctor_services = DoctorServices()

    def create_doctor_profile(self, data, user):
        try:

            doctor = self.doctor_services.get_doctor_factory().build_entity_with_id(
                specialization=data['specialization'], name=data['name'], doj=data['doj'],
                contact_no=data['contact_no'],
                user=user,
            )
            doctor.save()
            return doctor
        except Exception as e:
            raise Exception("Error in Doctor service:", e)
