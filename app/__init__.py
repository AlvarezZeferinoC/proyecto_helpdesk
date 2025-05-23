# app/__init__.py
from flask import Flask

def init_app():
    """
    Inicializa la aplicación Flask y registra las extensiones necesarias
    """
    app = Flask(__name__)
    return app