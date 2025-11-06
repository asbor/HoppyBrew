from pydantic import BaseSettings, ConfigDict


class Settings(BaseSettings):
    app_name: str = "Awesome API"

    model_config = ConfigDict(
        env_file=".env"
    )