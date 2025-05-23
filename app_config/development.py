# app_config/development.py
from app_config.default import Config

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'