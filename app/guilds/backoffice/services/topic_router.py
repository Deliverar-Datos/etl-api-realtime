from sqlalchemy.orm import Session
from app.events.schemas.base import EventTopic
from app.guilds.backoffice.schemas.events import IvaRespuestaData
from .processors.iva_respuesta_processor import IvaRespuestaProcessor
import logging

logger = logging.getLogger(__name__)

class BackofficeTopicRouter:
    @staticmethod
    def route(topic: str, payload: dict, db: Session):
        """
        Rutear eventos de backoffice a los procesadores apropiados
        
        Args:
            topic: Tópico del evento
            payload: Datos del evento
            db: Sesión de base de datos
            
        Returns:
            Resultado del procesamiento
            
        Raises:
            ValueError: Si el tópico no es soportado o hay errores de procesamiento
        """
        try:
            logger.info(f"Ruteando evento de backoffice: {topic}")
            
            if topic == EventTopic.IVA_RESPUESTA:
                logger.info("Procesando evento iva.respuesta")
                
                # Validar estructura completa del evento
                event_data = IvaRespuestaData(**payload)
                
                # Procesar con el payload validado
                result = IvaRespuestaProcessor.process(db, event_data.payload)
                
                # Crear objeto de respuesta consistente con otras guilds
                class ProcessingResult:
                    def __init__(self, processed_id: int, details: dict):
                        self.id = processed_id
                        self.details = details
                        
                    @property 
                    def processed_id(self):
                        return self.id
                
                # Usar el ID del primer pedido procesado o un valor por defecto
                processed_id = len(result.get('processed_orders', []))
                if processed_id == 0:
                    processed_id = 1  # Default para mantener consistencia
                
                response = ProcessingResult(processed_id, result)
                return response
                
            else:
                raise ValueError(f"Tópico de backoffice no soportado: {topic}")
                
        except Exception as e:
            logger.error(f"Error ruteando evento {topic}: {str(e)}")
            db.rollback()
            raise ValueError(f"Error procesando evento {topic}: {str(e)}")