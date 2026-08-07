from pydantic_settings import BaseSettings


class GeminiSettings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_MAX_OUTPUT_TOKENS: int = 500

    class Config:
        env_file = ".env"
        extra = "ignore"


gemini_settings = GeminiSettings()