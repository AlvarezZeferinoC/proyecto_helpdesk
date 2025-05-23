# app/utils/nlp_utils.py
import spacy
import nltk
from flask import current_app

# Descargar recursos de NLTK
def download_nltk_resources():
    resources = ['punkt', 'averaged_perceptron_tagger', 
                'maxent_ne_chunker', 'words', 'stopwords']
    for resource in resources:
        nltk.download(resource)

# Cargar modelo de spaCy
try:
    nlp = spacy.load('es_core_news_sm')
except:
    spacy.cli.download('es_core_news_sm')
    nlp = spacy.load('es_core_news_sm')

# Función para preparar el texto
def preprocess_text(text):
    return text.lower().strip()