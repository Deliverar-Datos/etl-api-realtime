from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import PedidoEnCamino
from app.guilds.repartidor.services.processors.utils_update_summary import update_fact_delivery_resumen_pedido, update_fact_repartidor_estadisticas

from datetime import datetime
from app.guilds.repartidor.models.star_schema import FactDeliveryEventos

def process(db: Session, data: PedidoEnCamino):
    """Process pedido en camino event"""
    try:
        print(f"Processing pedido en camino: {data}")

        # Buscar repartidor_id desde evento con estado ASIGNADO
        evento_asignado = db.query(FactDeliveryEventos).filter(
            FactDeliveryEventos.pedido_id == data.pedidoId,
            FactDeliveryEventos.estado == "ASIGNADO"
        ).first()
        repartidor_id = evento_asignado.repartidor_id if evento_asignado else None

        # Insertar o actualizar evento en fact_delivery_eventos
        evento = db.query(FactDeliveryEventos).filter(
            FactDeliveryEventos.pedido_id == data.pedidoId,
            FactDeliveryEventos.estado == data.estado
        ).first()
        if not evento:
            evento = FactDeliveryEventos(
                pedido_id=data.pedidoId,
                estado=data.estado,
                fecha_evento=datetime.utcnow(),
                repartidor_id=repartidor_id
            )
            db.add(evento)
        else:
            evento.fecha_evento = datetime.utcnow()
            evento.repartidor_id = repartidor_id

        db.commit()

        # Actualizar resumen y estadísticas
        update_fact_delivery_resumen_pedido(db, data.pedidoId)
        if repartidor_id:
            update_fact_repartidor_estadisticas(db, repartidor_id)

        return data
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error processing pedido en camino: {str(e)}")
