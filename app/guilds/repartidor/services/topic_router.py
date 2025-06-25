from sqlalchemy.orm import Session
from app.events.schemas.base import EventTopic
from app.guilds.repartidor.schemas.events import PedidoAceptado, PedidoAsignado, PedidoEntregado, PedidoArribo, DeliveryNuevoRepartidor, PedidoEnCamino
from app.guilds.repartidor.services.processors import pedido_aceptado_processor, pedido_asignado_processor, pedido_entregado_processor, pedido_arribo_processor, delivery_nuevo_repartidor_processor, pedido_en_camino_processor

class RepartidorTopicRouter:
    @staticmethod
    def route(topic: str, payload: dict, db: Session):
        """Route repartidor events to appropriate processors"""
        try:
            if topic == EventTopic.PEDIDO_ACEPTADO:
                data = PedidoAceptado(**payload)
                return pedido_aceptado_processor.process(db, data)
            elif topic == EventTopic.PEDIDO_ASIGNADO:
                data = PedidoAsignado(**payload)
                return pedido_asignado_processor.process(db, data)
            elif topic == EventTopic.PEDIDO_ENTREGADO:
                data = PedidoEntregado(**payload)
                return pedido_entregado_processor.process(db, data)
            elif topic == EventTopic.PEDIDO_ARRIBO:
                data = PedidoArribo(**payload)
                return pedido_arribo_processor.process(db, data)
            elif topic == EventTopic.DELIVERY_NUEVOREPARTIDOR:
                data = DeliveryNuevoRepartidor(**payload)
                return delivery_nuevo_repartidor_processor.process(db, data)
            elif topic == EventTopic.PEDIDO_ENCAMINO:
                data = PedidoEnCamino(**payload)
                return pedido_en_camino_processor.process(db, data)
            else:
                raise ValueError(f"Unsupported repartidor topic: {topic}")
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing {topic}: {str(e)}")
