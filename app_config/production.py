# app_config/production.py
from app_config.default import Config

class ProductionConfig(Config):
    ENV = 'production'
    CORS_ORIGINS = ['https://tu-dominio.com']