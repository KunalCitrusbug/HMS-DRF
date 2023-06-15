"""
This Following file will contain App level services functions that call domain layer
for instance and send back response to Interface layer.
"""
from HMS.domain.user.services import UserServices


class UserAppServices:
    def __init__(self):
        self.user_services = UserServices()

    def create_user(self, data):
        user = self.user_services.get_user_factory().build_entity_with_id(
            email=data['email'], is_active=True, is_admin=False, password=data['password'], user_type=data['user_type']
        )
        user.set_password(data['password'])
        user.save()
        return user
