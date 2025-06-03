# HelpDesk ChatBot para Empresa de Empastados

ChatBot inteligente para atención al cliente y soporte técnico en una empresa de empastados.

## Características principales
- Reconocimiento de intenciones del usuario
- Gestión de conversaciones contextuales
- Base de conocimiento para preguntas frecuentes
- Integración con tecnologías NLP (NLTK, spaCy)

## Estructura del proyecto
proyecto_helpdesk_2/
├── app/                          # Código principal de la aplicación
│   ├── data/                     # Datos estáticos (ej: knowledge_base.json)
│   ├── models/                   # Modelos de datos (analyzer.py, intent.py, etc.)
│   ├── nlp/                      # Procesamiento de lenguaje natural
│   ├── routes/                   # Rutas de la API (chat.py)
│   ├── services/                 # Lógica de negocio (intent_service.py, etc.)
│   ├── utils/                    # Utilidades compartidas (nlp_utils.py)
│   └── __init__.py               # Inicialización del módulo
├── app_config/                   # Configuraciones por entorno
│   ├── default.py                # Configuración base
│   ├── development.py            # Configuración para desarrollo
│   └── production.py             # Configuración para producción
├── static/                       # Archivos estáticos (CSS, JS)
│   ├── css/                      # Estilos (chat.css, style.css)
│   └── js/                       # Scripts (chat.js, utils.js)
├── templates/                    # Plantillas HTML (index.html)
├── tests/                        # Pruebas unitarias
│   ├── test_analyzer.py          # Pruebas para analyzer.py
│   ├── test_intent.py            # Pruebas para intent.py
│   └── test_response.py          # Pruebas para response.py
├── .env                          # Variables de entorno
├── app.py                        # Punto de entrada principal
├── config.py                     # Configuración general
└── requirements.txt              # Dependencias del proyecto


## Requisitos
- Python 3.8 >
- Flask
- Flask Cors
- spaCy
- es_core_news_md
- NLTK

## Instalación
1. Clonar repositorio
2. Crear entorno virtual: `python -m venv help-desk`
3. Activar entorno: `help-desk\Scripts\activate` (Windows) o `source help-desk/bin/activate` (Linux/Mac)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Descargar modelos de spaCy: `python -m spacy download es_core_news_md`
7. Ejecutar: `python app.py`