from sqlalchemy.orm import Session
from app.guilds.backoffice.models.tables import PedidoIva, SolicitudIva
from app.guilds.backoffice.schemas.events import IvaRespuestaData
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class IvaRespuestaProcessor:
    @staticmethod
    def process(db: Session, data: IvaRespuestaData):
        """Process IVA response events - stores received order data from Marketplace"""
        try:
            logger.info(f"Processing IVA response with {len(data.pedidos)} orders")
            
            processed_orders = []
            
            # Find the most recent solicitud to link with (optional)
            solicitud_reciente = db.query(SolicitudIva).filter(
                SolicitudIva.estado == 'ENVIADA'
            ).order_by(SolicitudIva.fecha_solicitud.desc()).first()
            
            for pedido_data in data.pedidos:
                # Check if pedido already exists (to avoid duplicates)
                existing_pedido = db.query(PedidoIva).filter(
                    PedidoIva.pedido_id == pedido_data.pedidoId,
                    PedidoIva.fecha_pedido == pedido_data.fecha
                ).first()
                
                if existing_pedido:
                    logger.warning(f"Order {pedido_data.pedidoId} already exists, skipping")
                    continue
                
                # Create new pedido IVA record
                pedido_iva = PedidoIva(
                    pedido_id=pedido_data.pedidoId,
                    fecha_pedido=pedido_data.fecha,
                    subtotal=pedido_data.subtotal,
                    monto_iva=pedido_data.montoIva,
                    total=pedido_data.total,
                    solicitud_id=solicitud_reciente.id if solicitud_reciente else None,
                    fecha_procesamiento=datetime.utcnow()
                )
                
                db.add(pedido_iva)
                processed_orders.append(pedido_iva)
            
            # Update solicitud status if linked
            if solicitud_reciente and processed_orders:
                solicitud_reciente.estado = 'PROCESADA'
            
            db.commit()
            
            # Refresh objects to get IDs
            for pedido in processed_orders:
                db.refresh(pedido)
            
            logger.info(f"Successfully processed {len(processed_orders)} IVA orders")
            return {
                "processed_orders": len(processed_orders),
                "orders": processed_orders,
                "solicitud_id": solicitud_reciente.id if solicitud_reciente else None
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error processing IVA response: {str(e)}")
            raise ValueError(f"Error processing IVA response: {str(e)}")