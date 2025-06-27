from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import PedidoAsignado
from app.guilds.repartidor.services.processors.utils_update_summary import update_fact_delivery_resumen_pedido, update_fact_repartidor_estadisticas

from app.guilds.repartidor.models.star_schema import DimRepartidor

from datetime import datetime
from app.guilds.repartidor.models.star_schema import FactDeliveryEventos

def process(db: Session, data: PedidoAsignado):
    """Process pedido asignado event"""
    try:
        print(f"Processing pedido asignado: {data}")

        # Buscar repartidor_id si no está presente, usando nombre, apellido y teléfono
        repartidor_id = None
        if hasattr(data, 'repartidor') and data.repartidor:
            repartidor_data = data.repartidor
            repartidor = db.query(DimRepartidor).filter(
                DimRepartidor.nombre == repartidor_data['nombre'],
                DimRepartidor.apellido == repartidor_data['apellido'],
                DimRepartidor.telefono == repartidor_data['telefono']
            ).first()
            if repartidor:
                repartidor_id = repartidor.repartidor_id

        # Insertar o actualizar evento en fact_delivery_eventos
        evento = db.query(FactDeliveryEventos).filter(FactDeliveryEventos.pedido_id == data.pedidoId, FactDeliveryEventos.estado == data.estado).first()
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
        if not repartidor_id:
            eventos = db.query(FactDeliveryEventos).filter_by(pedido_id=data.pedidoId).all()
            for evento in eventos:
                if evento.repartidor_id:
                    repartidor_id = evento.repartidor_id
                    break
        if repartidor_id:
            update_fact_repartidor_estadisticas(db, repartidor_id)

        return data
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error processing pedido asignado: {str(e)}")
