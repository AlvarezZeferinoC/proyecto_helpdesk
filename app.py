# app.py
import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from app_config import get_config
from app.routes.chat import chat_bp

def create_app(config_class=None):
    """
    Factory function que crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    # Cargar configuración
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # Configurar CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type", "X-Session-ID"]
        }
    })

    # Registrar el blueprint de chat
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    @app.route('/')
    def home():
        """Renderiza la página principal del chat"""
        return render_template('index.html')

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Recurso no encontrado'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Error interno del servidor'}), 500

    return app


def main():
    """
    Función principal que crea y ejecuta la aplicación
    """
    env = os.getenv('FLASK_ENV', 'development')
    debug = env == 'development'

    app = create_app()

    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))

    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()