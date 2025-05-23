# app.py
from flask import Flask
from flask_cors import CORS
from app_config import get_config
from app.routes.chat import chat_bp


def create_app(config_class=None):
    app = Flask(__name__)

    # Cargar configuración
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # Inicializar CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    # Registrar blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
