from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    upload_dir: str = "./storage/resumes"
    max_file_size_mb: int = 5
    database_url: str
    gemini_api_key: str
    storage_backend: str = "local"  # "local" or "s3"
    s3_bucket_name: str = ""
    aws_region: str = "us-east-1"

    class Config:
        env_file = ".env"

settings = Settings()

