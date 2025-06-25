from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.guilds.backoffice.models.tables import PedidoIva
from app.guilds.backoffice.schemas.events import IvaRespuestaPayload
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class IvaRespuestaProcessor:
    @staticmethod
    def process(db: Session, payload: IvaRespuestaPayload) -> Dict[str, Any]:
        """
        Procesar evento iva.respuesta almacenando pedidos con información de IVA
        
        Args:
            db: Sesión de base de datos
            payload: Datos validados del evento
            
        Returns:
            Diccionario con resultado del procesamiento
            
        Raises:
            ValueError: Si hay errores en el procesamiento
        """
        try:
            processed_orders = []
            skipped_orders = []
            total_iva_procesado = 0.0
            
            logger.info(f"Procesando {len(payload.pedidos)} pedidos con IVA")
            
            for pedido_data in payload.pedidos:
                try:
                    # Verificar si el pedido ya existe
                    existing_pedido = db.query(PedidoIva).filter(
                        PedidoIva.pedido_id == pedido_data.pedidoId
                    ).first()
                    
                    if existing_pedido:
                        logger.warning(f"Pedido {pedido_data.pedidoId} ya existe, omitiendo")
                        skipped_orders.append({
                            "pedido_id": pedido_data.pedidoId,
                            "razon": "Ya existe en base de datos"
                        })
                        continue
                    
                    # Calcular porcentaje de IVA
                    porcentaje_iva = pedido_data.porcentaje_iva
                    
                    # Crear nuevo registro
                    nuevo_pedido = PedidoIva(
                        pedido_id=pedido_data.pedidoId,
                        fecha_pedido=pedido_data.fecha,
                        subtotal=pedido_data.subtotal,
                        monto_iva=pedido_data.montoIva,
                        total=pedido_data.total,
                        porcentaje_iva=porcentaje_iva
                    )
                    
                    db.add(nuevo_pedido)
                    db.flush()  # Para obtener el ID sin hacer commit
                    
                    processed_orders.append(nuevo_pedido.resumen)
                    total_iva_procesado += pedido_data.montoIva
                    
                    logger.info(f"Pedido {pedido_data.pedidoId} procesado exitosamente")
                    
                except IntegrityError as e:
                    logger.error(f"Error de integridad para pedido {pedido_data.pedidoId}: {str(e)}")
                    db.rollback()
                    skipped_orders.append({
                        "pedido_id": pedido_data.pedidoId,
                        "razon": "Error de integridad de datos"
                    })
                    continue
                    
            # Commit solo si hay pedidos procesados exitosamente
            if processed_orders:
                db.commit()
                logger.info(f"Commit exitoso: {len(processed_orders)} pedidos procesados")
            else:
                logger.warning("No se procesaron pedidos nuevos")
            
            # Preparar respuesta
            result = {
                "processed_count": len(processed_orders),
                "skipped_count": len(skipped_orders),
                "total_iva_procesado": round(total_iva_procesado, 2),
                "processed_orders": processed_orders,
                "skipped_orders": skipped_orders,
                "statistics": {
                    "total_pedidos_evento": len(payload.pedidos),
                    "total_iva_evento": payload.total_iva,
                    "total_general_evento": payload.total_general,
                    "promedio_iva_por_pedido": round(payload.total_iva / len(payload.pedidos), 2) if payload.pedidos else 0
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando evento iva.respuesta: {str(e)}")
            db.rollback()
            raise ValueError(f"Error procesando evento iva.respuesta: {str(e)}")
    
    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        """Obtener estadísticas de pedidos IVA procesados"""
        try:
            from sqlalchemy import func
            
            stats = db.query(
                func.count(PedidoIva.id).label('total_pedidos'),
                func.sum(PedidoIva.monto_iva).label('total_iva'),
                func.sum(PedidoIva.total).label('total_general'),
                func.avg(PedidoIva.porcentaje_iva).label('promedio_porcentaje_iva'),
                func.min(PedidoIva.fecha_pedido).label('primer_pedido'),
                func.max(PedidoIva.fecha_pedido).label('ultimo_pedido')
            ).first()
            
            return {
                "total_pedidos": int(stats.total_pedidos or 0),
                "total_iva": float(stats.total_iva or 0),
                "total_general": float(stats.total_general or 0),
                "promedio_porcentaje_iva": float(stats.promedio_porcentaje_iva or 0),
                "primer_pedido": stats.primer_pedido.isoformat() if stats.primer_pedido else None,
                "ultimo_pedido": stats.ultimo_pedido.isoformat() if stats.ultimo_pedido else None
            }
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {str(e)}")
            return {}