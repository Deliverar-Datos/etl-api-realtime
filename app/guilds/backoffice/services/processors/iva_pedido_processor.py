from sqlalchemy.orm import Session
from app.guilds.backoffice.models.tables import SolicitudIva
from app.guilds.backoffice.schemas.events import IvaPedidoData
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class IvaPedidoProcessor:
    @staticmethod
    def process(db: Session, data: IvaPedidoData):
        """Process IVA request events - tracks outgoing requests to Marketplace"""
        try:
            logger.info(f"Processing IVA request from {data.fechaDesde} to {data.fechaHasta}")
            
            # Create solicitud record to track the request
            solicitud = SolicitudIva(
                fecha_desde=data.fechaDesde,
                fecha_hasta=data.fechaHasta,
                fecha_solicitud=datetime.utcnow(),
                estado='ENVIADA'
            )
            
            db.add(solicitud)
            db.commit()
            db.refresh(solicitud)
            
            logger.info(f"IVA request tracked with ID: {solicitud.id}")
            return solicitud
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error processing IVA request: {str(e)}")
            raise ValueError(f"Error processing IVA request: {str(e)}")