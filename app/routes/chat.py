# app/routes/chat.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..nlp.analyzer import TextAnalyzer
from ..nlp.intent import IntentRecognizer
from ..nlp.response import ResponseGenerator
import json
from pathlib import Path
import uuid
from http import HTTPStatus

# Crear el blueprint para el chat
chat_bp = Blueprint('chat', __name__)

# Cargar la base de conocimientos
kb_path = Path(__file__).parent.parent / 'data' / 'knowledge_base.json'
with open(kb_path, 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)

# Inicializar componentes NLP
text_analyzer = TextAnalyzer()
intent_recognizer = IntentRecognizer(text_analyzer)
response_generator = ResponseGenerator(knowledge_base)

# Almacenamiento temporal de mensajes (en producción debería usar una base de datos)
chat_sessions = {}


@chat_bp.route('/messages', methods=['GET'])
def get_messages():
    """
    Endpoint para obtener los mensajes de una sesión específica
    """
    session_id = request.args.get('session_id')
    if not session_id or session_id not in chat_sessions:
        return jsonify({
            'status': 'error',
            'message': 'Sesión no válida'
        }), HTTPStatus.BAD_REQUEST

    return jsonify({
        'status': 'success',
        'messages': chat_sessions[session_id]
    })


@chat_bp.route('/message', methods=['POST'])
def send_message():
    """Endpoint para procesar un mensaje y generar una respuesta"""
    try:
        # Validar el contenido de la solicitud
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'El contenido debe ser JSON'
            }), HTTPStatus.BAD_REQUEST

        data = request.json
        if not data or 'message' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionó un mensaje'
            }), HTTPStatus.BAD_REQUEST

        user_message = data['message'].strip()
        session_id = data.get('session_id', str(uuid.uuid4()))

        # Validar longitud del mensaje
        if len(user_message) == 0:
            return jsonify({
                'status': 'error',
                'message': 'El mensaje no puede estar vacío'
            }), HTTPStatus.BAD_REQUEST

        if len(user_message) > 1000:
            return jsonify({
                'status': 'error',
                'message': 'El mensaje no puede exceder los 1000 caracteres'
            }), HTTPStatus.BAD_REQUEST

        # Inicializar la sesión si no existe
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []

        # Crear y guardar el mensaje del usuario
        user_message_obj = {
            'id': str(uuid.uuid4()),
            'content': user_message,
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'user'
        }
        chat_sessions[session_id].append(user_message_obj)

        # Procesar el mensaje con NLP
        intent_data = intent_recognizer.recognize(user_message)
        bot_response = response_generator.generate_response(intent_data)

        # Crear y guardar la respuesta del bot
        bot_response_obj = {
            'id': str(uuid.uuid4()),
            'content': bot_response,
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'bot',
            'intent_data': intent_data
        }
        chat_sessions[session_id].append(bot_response_obj)

        return jsonify({
            'status': 'success',
            'message': bot_response_obj,
            'session_id': session_id
        }), HTTPStatus.OK

    except Exception as e:
        # Log del error (deberías implementar un sistema de logging apropiado)
        print(f"Error processing chat message: {str(e)}")

        return jsonify({
            'status': 'error',
            'message': 'Error interno del servidor'
        }), HTTPStatus.INTERNAL_SERVER_ERROR


@chat_bp.route('/clear', methods=['POST'])
def clear_chat():
    """
    Endpoint para limpiar el historial de una sesión de chat
    """
    session_id = request.json.get('session_id')
    if not session_id:
        return jsonify({
            'status': 'error',
            'message': 'Se requiere session_id'
        }), HTTPStatus.BAD_REQUEST

    if session_id in chat_sessions:
        chat_sessions[session_id] = []

    return jsonify({
        'status': 'success',
        'message': 'Chat limpiado exitosamente'
    })


@chat_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar el estado del servicio
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), HTTPStatus.OK
