# app/services/response_service.py
class ResponseService:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def generate_response(self, intent_data):
        # Lógica movida desde el ResponseGenerator original
        pass

    def get_default_response(self):
        return "Lo siento, no pude entender tu pregunta. ¿Podrías reformularla?"
