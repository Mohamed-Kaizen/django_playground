import uuid
from typing import Any, Dict

from loguru import logger

from analytics.signal import analytic_signal
from users.models import CustomUser


class AuthorInterface:
    @staticmethod
    def get_author(*, author_id: uuid.UUID) -> Dict[str, Any]:
        return {"author_name": CustomUser.objects.get(user_uuid=author_id).username}


class AnalyticInterface:
    @staticmethod
    def create_analytic(*, model: Any, instance: Any, request: Any) -> None:
        analytic_signal.send(sender=model, instance=instance, request=request)

        logger.success(f"analytic data was created for {instance}")
