import json
from pathlib import Path


class IntentRecognizer:
    def __init__(self, analyzer):
        """
        Inicializa el reconocedor de intenciones
        Args:
            analyzer: Instancia de TextAnalyzer
        """
        self.analyzer = analyzer
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Carga la base de conocimientos desde el archivo JSON"""
        kb_path = Path(__file__).parent.parent / 'data' / 'knowledge_base.json'
        with open(kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def recognize(self, text):
        """
        Reconoce la intención en el texto del usuario
        Args:
            text (str): Texto del usuario
        Returns:
            dict: Intención reconocida y entidades
        """
        # Analizar el texto
        analysis = self.analyzer.analyze(text)

        # Identificar intención
        intent_scores = self._score_intents(analysis)

        # Extraer entidades
        entities = self._extract_entities(text)

        # Obtener la intención con mayor puntaje
        intent = max(intent_scores.items(), key=lambda x: x[1])[
            0] if intent_scores else None

        return {
            'intent': intent,
            'entities': entities,
            'confidence': intent_scores.get(intent, 0),
            'analysis': analysis
        }

    def _score_intents(self, analysis):
        """
        Calcula el puntaje para cada intención posible
        Args:
            analysis (dict): Análisis del texto
        Returns:
            dict: Puntajes para cada intención
        """
        scores = {}

        for intent, intent_data in self.knowledge_base.items():
            score = 0
            # Verificar patrones en tokens y lemmas
            for pattern in intent_data['patterns']:
                if pattern in analysis['lemmas'] or pattern in analysis['tokens']:
                    score += 1

            if score > 0:
                scores[intent] = score

        return scores

    def _extract_entities(self, text):
        """
        Extrae entidades del texto
        Args:
            text (str): Texto a analizar
        Returns:
            dict: Entidades encontradas
        """
        entities = {}

        # Diccionario de patrones para tipos de servicio
        service_patterns = {
            'tesis': ['tesis', 'tesina', 'trabajo final'],
            'libro': ['libro', 'libros', 'ejemplar'],
            'revista': ['revista', 'revistas', 'publicación']
        }

        # Diccionario de patrones para tipos de material
        material_patterns = {
            'tapa_dura': ['tapa dura', 'pasta dura'],
            'rustica': ['rustica', 'tapa blanda'],
            'espiral': ['espiral', 'anillas']
        }

        text_lower = text.lower()

        # Buscar coincidencias de tipo de servicio
        for service, patterns in service_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                entities['tipo_servicio'] = service
                break

        # Buscar coincidencias de tipo de material
        for material, patterns in material_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                entities['tipo_material'] = material
                break

        return entities
