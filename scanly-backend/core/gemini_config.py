from pydantic_settings import BaseSettings


class GeminiSettings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.6-flash"
    GEMINI_MAX_OUTPUT_TOKENS: int = 1024
    GEMINI_TIMEOUT_SECONDS: int = 15

    class Config:
        env_file = ".env"
        extra = "ignore"


gemini_settings = GeminiSettings()