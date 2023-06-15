"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to the Interface layer.
"""
from HMS.domain.staff.services import StaffServices


class StaffAppServices:
    def __init__(self):
        self.staff_services = StaffServices()

    def create_staff_profile(self, data, user):
        try:

            staff = self.staff_services.get_staff_factory().build_entity_with_id(
                specialization=data['specialization'], name=data['name'], doj=data['doj'],
                contact_no=data['contact_no'], staff_type=data['staff_type'], user=user)
            staff.save()
            return staff
        except Exception as e:
            raise Exception("Error in Staff service:", e)
