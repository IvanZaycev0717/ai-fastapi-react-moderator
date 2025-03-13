from __future__ import annotations


from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.auth import APIKeyAuth

from schemas.envs import Settings
from settings import AI_MODERATOR_REQUEST

settings = Settings()


async def moderate_comment(original_text: str) -> str:
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
        folder_id=settings.yc_folder_id,
        auth=APIKeyAuth(settings.yc_secret_key),
        enable_server_data_logging=False,
    )
    result = (
        sdk.models.completions(
            "yandexgpt").configure(temperature=0.5).run(messages)
    )
    return result.alternatives[0].text
