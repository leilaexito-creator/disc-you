from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Database
    database_url: str = "sqlite:////tmp/empathic_ai.db"
    redis_url: str = "redis://localhost:6379/0"
    
    # LLM
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    llm_provider: str = "openai"  # openai or anthropic
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App
    app_name: str = "Empathic AI Coach"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # Emotional Safety
    max_conversation_length: int = 50
    context_window: int = 10
    rate_limit_requests: int = 100
    rate_limit_period: int = 3600
    
    # Monitoring
    log_level: str = "INFO"
    enable_audit_logs: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
