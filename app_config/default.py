# app_config/default.py

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your-secret-key'
    CORS_ORIGINS = ['http://localhost:5000']
    SESSION_LIFETIME = 3600
    NLP_MODEL = 'es_core_news_sm'