# app/nlp/entities.py
from typing import Dict, List, Optional
import re
from datetime import datetime

class EntityExtractor:
    """Clase para extracción de entidades del texto"""
    
    def __init__(self):
        # Expresiones regulares para tipos de entidades comunes
        self.patterns = {
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'phone': r'(?:\+34|0034)?[6789]\d{8}',
            'url': r'https?://(?:[\w-]|(?:%[\da-fA-F]{2}))+[^\s]*',
            'dimensions': r'\d+(?:[.,]\d+)?\s*(?:cm|mm|metros?|pulgadas?)',
            'price': r'(?:€|\$)?\s*\d+(?:[.,]\d{2})?(?:\s*(?:euros?|EUR))?'
        }
        
        # Diccionario de materiales y sus variantes
        self.materials = {
            'tapa_dura': [
                'tapa dura', 'pasta dura', 'hardcover', 
                'tapa rigida', 'encuadernación dura'
            ],
            'rustica': [
                'rústica', 'tapa blanda', 'paperback', 
                'tapa suave', 'encuadernación suave'
            ],
            'espiral': [
                'espiral', 'wire-o', 'anillado', 
                'encuadernación espiral', 'gusanillo'
            ],
            'cosido': [
                'cosido', 'costura', 'sewn binding', 
                'encuadernación cosida'
            ]
        }
        
        # Diccionario de tipos de documentos
        self.document_types = {
            'tesis': [
                'tesis', 'tesina', 'trabajo final', 
                'trabajo de grado', 'tfg', 'tfm'
            ],
            'libro': [
                'libro', 'novela', 'poemario', 
                'manual', 'guía', 'textbook'
            ],
            'revista': [
                'revista', 'magazine', 'publicación periódica', 
                'journal', 'boletín'
            ],
            'documento': [
                'documento', 'informe', 'reporte', 
                'memoria', 'proyecto'
            ]
        }

    def extract_all(self, text: str) -> Dict:
        """
        Extrae todas las entidades posibles del texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con todas las entidades encontradas
        """
        entities = {}
        
        # Extraer entidades básicas
        for entity_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            entities[entity_type] = [m.group() for m in matches]
        
        # Extraer material
        material = self._find_material(text)
        if material:
            entities['material'] = material
            
        # Extraer tipo de documento
        doc_type = self._find_document_type(text)
        if doc_type:
            entities['tipo_documento'] = doc_type
            
        # Extraer fechas y plazos
        dates = self._extract_dates(text)
        if dates:
            entities['fechas'] = dates
            
        # Extraer cantidades
        quantities = self._extract_quantities(text)
        if quantities:
            entities['cantidades'] = quantities
            
        return entities

    def _find_material(self, text: str) -> Optional[str]:
        """
        Identifica el tipo de material mencionado en el texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Tipo de material o None si no se encuentra
        """
        text = text.lower()
        for material, variants in self.materials.items():
            if any(variant in text for variant in variants):
                return material
        return None

    def _find_document_type(self, text: str) -> Optional[str]:
        """
        Identifica el tipo de documento mencionado en el texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Tipo de documento o None si no se encuentra
        """
        text = text.lower()
        for doc_type, variants in self.document_types.items():
            if any(variant in text for variant in variants):
                return doc_type
        return None

    def _extract_dates(self, text: str) -> List[Dict]:
        """
        Extrae referencias a fechas y plazos del texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Lista de fechas y plazos encontrados
        """
        dates = []
        
        # Patrones de fecha común
        date_patterns = [
            (r'\d{1,2}/\d{1,2}/\d{2,4}', 'fecha_exacta'),
            (r'\d{1,2} de (?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)', 'fecha_mes'),
            (r'próximo (?:lunes|martes|miércoles|jueves|viernes|sábado|domingo)', 'fecha_relativa'),
            (r'(?:esta|próxima|siguiente) semana', 'plazo_semana'),
            (r'(?:este|próximo|siguiente) mes', 'plazo_mes')
        ]
        
        for pattern, date_type in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                dates.append({
                    'texto': match.group(),
                    'tipo': date_type,
                    'posicion': match.span()
                })
                
        return dates

    def _extract_quantities(self, text: str) -> List[Dict]:
        """
        Extrae cantidades y unidades del texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Lista de cantidades encontradas
        """
        quantities = []
        
        # Patrones de cantidad
        quantity_patterns = [
            (r'\d+(?:[.,]\d+)?\s*(?:páginas?|hojas?|folios?)', 'paginas'),
            (r'\d+(?:[.,]\d+)?\s*(?:copias?|ejemplares?)', 'copias'),
            (r'\d+(?:[.,]\d+)?\s*(?:cm|mm|metros?|pulgadas?)', 'dimensiones'),
            (r'\d+(?:[.,]\d+)?\s*(?:€|euros?|EUR|\$)', 'precio')
        ]
        
        for pattern, qty_type in quantity_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                value = re.search(r'\d+(?:[.,]\d+)?', match.group())
                if value:
                    quantities.append({
                        'valor': float(value.group().replace(',', '.')),
                        'texto': match.group(),
                        'tipo': qty_type,
                        'posicion': match.span()
                    })
                    
        return quantities