from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Habits backend"
    VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///./habit_tracker.db"

    class Config:
        case_sensitive = True

settings = Settings()