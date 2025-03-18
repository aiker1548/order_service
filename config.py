import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Настройки для подключения к базе данных
    MONGODB_URL: str = "mongodb://admin:secret@127.0.0.1:27017/?authSource=admin"
    MONGODB_DB_NAME: str = "orders" 
    # Настройки для приложения
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    APP_DEBUG: bool = True  # Включить отладку (для разработки)
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")  # Используй более безопасный ключ в продакшн
    ALGORITHM: str = "HS256"  # Алгоритм для JWT (если решишь использовать)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Время жизни токена

    # Настройки для безопасности
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")  # Используй более безопасный ключ в продакшн
    ALGORITHM: str = "HS256"  # Алгоритм для JWT (если решишь использовать)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Время жизни токена

    # Дополнительные настройки (например, для CORS, логирования и др.)
    CORS_ORIGINS: list[str] = ["*"]  # Настройки CORS (все домены, можно ограничить)
    
    # Настройки для мидлвар
    MAX_REQUEST_SIZE: int = 10485760  # 10MB, если нужно ограничить размер запроса

    #Настройка kafka
    bootstrap_servers: str = "localhost:9093"
    group_id: str = "my-group"
    auto_offset_reset: str = "earliest"
    enable_auto_commit: bool = True
    auto_commit_interval_ms: int = 5000
    max_poll_records: int = 500
    request_topic: str = "user_info_request"
    response_topic: str = "user_info_response"

    class Config:
        env_file = ".env"  # Путь к файлу .env


# Загружаем конфигурацию
config = Settings()