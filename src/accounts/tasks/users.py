import uuid

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

logger = get_task_logger(__name__)


@shared_task(name="myproject.users.send_sms")
def send_sms(username: str, message: str) -> None:
    data = {
        "api_token": settings.SSL_TOKEN,
        "sid": settings.SSL_SID,
        "csms_id": uuid.uuid1().hex[:20],
        "sms": message,
        "msisdn": username,
    }
    requests.post(settings.SSL_URL, data=data)
    logger.info(message)
    return
