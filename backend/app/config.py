from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    database_url:str="sqlite+aiosqlite:///./careerflow.db"
    jwt_secret:str="development-secret-change-in-production"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
