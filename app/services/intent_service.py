# app/services/intent_service.py
from ..models.intent import IntentRecognizer
from ..models.analyzer import GrammaticalAnalyzer


class IntentService:
    def __init__(self, knowledge_base):
        self.intent_recognizer = IntentRecognizer(knowledge_base)
        self.analyzer = GrammaticalAnalyzer()

    def process_query(self, text):
        analysis = self.analyzer.analyze(text)
        return self.intent_recognizer.recognize(text)
