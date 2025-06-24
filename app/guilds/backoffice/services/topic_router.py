from sqlalchemy.orm import Session
from app.events.schemas.base import EventTopic
from app.guilds.backoffice.schemas.events import IvaPedidoData, IvaRespuestaData
from .processors.iva_pedido_processor import IvaPedidoProcessor
from .processors.iva_respuesta_processor import IvaRespuestaProcessor
import logging

logger = logging.getLogger(__name__)

class BackofficeTopicRouter:
    @staticmethod
    def route(topic: str, payload: dict, db: Session):
        """Route backoffice events to appropriate processors"""
        try:
            logger.info(f"Routing backoffice event: {topic}")
            
            if topic == EventTopic.IVA_PEDIDO:
                logger.info("Processing IVA Pedido (outgoing request)")
                # Validate payload directly as IvaPedidoData
                data = IvaPedidoData(**payload)
                return IvaPedidoProcessor.process(db, data)
                
            elif topic == EventTopic.IVA_RESPUESTA:
                logger.info("Processing IVA Respuesta (incoming response)")
                # Validate payload directly as IvaRespuestaData
                data = IvaRespuestaData(**payload)
                result = IvaRespuestaProcessor.process(db, data)
                return result
                
            else:
                raise ValueError(f"Unsupported backoffice topic: {topic}")
                
        except Exception as e:
            db.rollback()
            logger.error(f"Error processing backoffice topic {topic}: {str(e)}")
            raise ValueError(f"Error processing {topic}: {str(e)}")