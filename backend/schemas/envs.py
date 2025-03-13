from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    yc_folder_id: str
    yc_secret_key: str
