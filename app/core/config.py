from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    port: int = Field(default=8000, alias="PORT")
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_model: str = Field(
        default="meta-llama/llama-3.1-8b-instruct", alias="OPENROUTER_MODEL"
    )
    llm_enabled: bool = Field(default=True, alias="LLM_ENABLED")
    llm_confidence_threshold: float = Field(default=0.70, alias="LLM_CONFIDENCE_THRESHOLD")
    llm_timeout_seconds: float = Field(default=8.0, alias="LLM_TIMEOUT_SECONDS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    app_env: str = Field(default="production", alias="APP_ENV")
    max_message_length: int = 5000

    @property
    def llm_available(self) -> bool:
        return self.llm_enabled and bool(self.openrouter_api_key.strip())


def get_settings() -> Settings:
    return Settings()
