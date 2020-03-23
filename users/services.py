from typing import Dict

from .models import CustomUser


class UserService:
    @staticmethod
    def get_all_users() -> CustomUser:
        return CustomUser.objects.all()

    @staticmethod
    def create_user(*, data: Dict) -> CustomUser:

        password = data.pop("password")

        user = CustomUser(**data)

        user.set_password(password)

        user.save()

        return user
