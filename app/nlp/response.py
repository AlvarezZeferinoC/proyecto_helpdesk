class ResponseGenerator:
    def __init__(self, knowledge_base):
        """
        Inicializa el generador de respuestas
        Args:
            knowledge_base (dict): Base de conocimientos
        """
        self.knowledge_base = knowledge_base

    def generate_response(self, intent_data):
        """
        Genera una respuesta basada en la intención y entidades reconocidas
        Args:
            intent_data (dict): Datos de la intención reconocida
        Returns:
            str: Respuesta generada
        """
        intent = intent_data['intent']
        entities = intent_data['entities']

        if not intent:
            return self._get_default_response()

        intent_info = self.knowledge_base.get(intent)
        if not intent_info:
            return self._get_default_response()

        # Construir respuesta
        response_parts = []

        # Agregar respuesta default de la intención
        response_parts.append(intent_info['responses']['default'])

        # Agregar respuestas específicas basadas en entidades
        for entity_type, entity_value in entities.items():
            if entity_value in intent_info['responses']:
                response_parts.append(intent_info['responses'][entity_value])

        # Si no hay entidades específicas, agregar todas las opciones
        if not entities:
            for key, value in intent_info['responses'].items():
                if key != 'default':
                    response_parts.append(value)

        return '\n'.join(response_parts)

    def _get_default_response(self):
        """
        Genera una respuesta por defecto cuando no se reconoce la intención
        Returns:
            str: Respuesta por defecto
        """
        return ("Lo siento, no pude entender tu pregunta. ¿Podrías reformularla? "
                "Por ejemplo:\n"
                "- ¿Cuánto cuesta encuadernar una tesis?\n"
                "- ¿Qué tipos de materiales usan?\n"
                "- ¿Cuánto tiempo tarda la encuadernación?")
