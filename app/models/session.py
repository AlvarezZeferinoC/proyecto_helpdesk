# app/models/session.py
from datetime import datetime


class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.last_intent = None
        self.conversation_history = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_interaction(self, intent_data):
        self.last_intent = intent_data['intent']
        self.conversation_history.append({
            'intent': intent_data['intent'],
            'entities': intent_data['entities'],
            'timestamp': datetime.now()
        })
        self.updated_at = datetime.now()
