from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import PedidoCancelado
from app.guilds.repartidor.services.processors.utils_update_summary import update_fact_delivery_resumen_pedido, update_fact_repartidor_estadisticas
from datetime import datetime
from app.guilds.repartidor.models.star_schema import FactDeliveryEventos

def process(db: Session, data: PedidoCancelado):
    """Process pedido cancelado event"""
    try:
        print(f"Processing pedido cancelado: {data}")

        # Buscar repartidor_id desde evento con estado ASIGNADO
        evento_asignado = db.query(FactDeliveryEventos).filter(
            FactDeliveryEventos.pedido_id == data.pedidoId,
            FactDeliveryEventos.estado == "ASIGNADO"
        ).first()
        repartidor_id = evento_asignado.repartidor_id if evento_asignado else None

        # Si no se encontró repartidor_id, intentar obtenerlo desde resumen
        if not repartidor_id:
            resumen = db.query(FactDeliveryResumenPedido).filter(FactDeliveryResumenPedido.pedido_id == data.pedidoId).first()
            repartidor_id = resumen.repartidor_id if resumen else None

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
        # Obtener repartidor_id solo desde evento ASIGNADO para actualizar estadísticas
        evento_asignado = db.query(FactDeliveryEventos).filter(
            FactDeliveryEventos.pedido_id == data.pedidoId,
            FactDeliveryEventos.estado == "ASIGNADO"
        ).first()
        repartidor_id_asignado = evento_asignado.repartidor_id if evento_asignado else None
        if repartidor_id_asignado:
            update_fact_repartidor_estadisticas(db, repartidor_id_asignado)

        return data
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error processing pedido cancelado: {str(e)}")
