import uuid
from typing import Any, Dict

from loguru import logger

from analytics.signal import analytic_signal
from users.models import CustomUser


class UserInterface:
    @staticmethod
    def get_username(*, user_id: uuid.UUID) -> Dict[str, Any]:
        return {"username": CustomUser.objects.get(user_uuid=user_id).username}

    @staticmethod
    def get_user(*, username: str) -> Dict[str, CustomUser]:
        return {"username": CustomUser.objects.get(username=username)}


class AnalyticInterface:
    @staticmethod
    def create_analytic(*, model: Any, instance: Any, request: Any) -> None:
        analytic_signal.send(sender=model, instance=instance, request=request)

        logger.success(f"analytic data was created for {instance}")
