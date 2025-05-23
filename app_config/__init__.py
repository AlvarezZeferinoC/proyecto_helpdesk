# app_config/__init__.py
import os
from app_config.development import DevelopmentConfig
from app_config.production import ProductionConfig

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    env = os.getenv('FLASK_ENV', 'default')
    return config[env]