from pydantic_settings import BaseSettings, SettingsConfigDict

from settings import ENVIROMENT_FILE


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENVIROMENT_FILE)

    yc_folder_id: str
    yc_secret_key: str
