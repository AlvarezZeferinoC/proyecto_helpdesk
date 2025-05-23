import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Descargar recursos necesarios
nltk.download('punkt')
nltk.download('stopwords')


class TextAnalyzer:
    def __init__(self):
        """Inicializa el analizador de texto con los modelos necesarios"""
        self.nlp = spacy.load('es_core_news_sm')
        self.stop_words = set(stopwords.words('spanish'))

    def analyze(self, text):
        """
        Analiza un texto y retorna información lingüística relevante
        Args:
            text (str): Texto a analizar
        Returns:
            dict: Información lingüística del texto
        """
        # Procesar el texto con spaCy
        doc = self.nlp(text.lower())

        # Análisis básico
        analysis = {
            'tokens': [token.text for token in doc],
            'lemmas': [token.lemma_ for token in doc],
            'pos_tags': [token.pos_ for token in doc],
            'entities': [(ent.text, ent.label_) for ent in doc.ents],
            'non_stop_words': [token.text for token in doc if token.text not in self.stop_words]
        }

        return analysis

    def extract_key_phrases(self, text):
        """
        Extrae frases clave del texto
        Args:
            text (str): Texto a analizar
        Returns:
            list: Lista de frases clave
        """
        doc = self.nlp(text.lower())
        key_phrases = []

        # Extraer sustantivos y sus modificadores
        for chunk in doc.noun_chunks:
            key_phrases.append(chunk.text)

        return key_phrases

    def get_main_action(self, text):
        """
        Identifica la acción principal en la pregunta
        Args:
            text (str): Texto a analizar
        Returns:
            str: Acción principal identificada
        """
        doc = self.nlp(text.lower())

        # Buscar el verbo principal
        main_verb = None
        for token in doc:
            if token.pos_ == "VERB":
                main_verb = token.lemma_
                break

        return main_verb
