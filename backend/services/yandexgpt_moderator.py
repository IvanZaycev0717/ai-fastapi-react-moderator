from __future__ import annotations
import os
from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.auth import APIKeyAuth
from dotenv import load_dotenv

from settings import AI_MODERATOR_REQUEST

load_dotenv()


def moderate_comment(original_text: str) -> str:
    messages = [
        {
            "role": "system",
            "text": AI_MODERATOR_REQUEST
        },
        {
            "role": "user",
            "text": original_text,
        },
    ]

    sdk = YCloudML(
        folder_id=os.getenv('YC_FOLDER_ID'),
        auth=APIKeyAuth(os.getenv('YC_SECRET_KEY')),
        enable_server_data_logging=False,
    )
    result = (
        sdk.models.completions(
            "yandexgpt").configure(temperature=0.5).run(messages)
    )
    return result.alternatives[0].text
