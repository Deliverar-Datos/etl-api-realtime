from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Any, Optional
from app.events.schemas.base import EventTopic
from app.models.database import get_db
from app.guilds.blockchain.services.topic_router import BlockchainTopicRouter
from app.guilds.marketplace.services.topic_router import MarketplaceTopicRouter
from app.guilds.bi.services.topic_router import DashboardBiTopicRouter
from app.guilds.repartidor.services.topic_router import RepartidorTopicRouter
from app.guilds.backoffice.services.topic_router import BackofficeTopicRouter
import logging
from fastapi.responses import PlainTextResponse

logger = logging.getLogger(__name__)
router = APIRouter()

BI_TOPICS = {
    EventTopic.PROMO_REGISTRADA,
    EventTopic.PROMO_COMERCIO_ASOCIADA,
    EventTopic.PROMO_TENANT_ASOCIADA,
    EventTopic.ORDEN_REGISTRADA,
    EventTopic.ORDEN_ESTADO_ACTUALIZADO,
    EventTopic.CLIENT_REGISTRADO,
    EventTopic.DELIVERY_REGISTRADO,
    EventTopic.TRANSACCION_BLOCKCHAIN_REGISTRADA,
    EventTopic.COMERCIO_CREADO,
    EventTopic.TENANT_CREADO
}

def _get_bi_processed_id(result: Any) -> Optional[int]:
    """Helper para obtener el ID procesado del resultado de BI"""
    if hasattr(result, 'id'): return result.id
    if hasattr(result, 'client_id'): return result.client_id
    if hasattr(result, 'delivery_id'): return result.delivery_id
    if hasattr(result, 'order_id'): return result.order_id
    if hasattr(result, 'transaction_id'): return result.transaction_id
    if hasattr(result, 'commerce_id'): return result.commerce_id
    if hasattr(result, 'tenant_id'): return result.tenant_id
    if isinstance(result, dict) and 'promo_id' in result: return result['promo_id']
    return None


@router.post("/callback")
async def handle_event(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Manejo de eventos entrantes por topic.
    """

    try:
        payload_data = await request.json()
        topic_str = payload_data.get("topic")
        event_payload = payload_data.get("payload")

        if not topic_str:
            raise HTTPException(status_code=400, detail="Falta 'topic' en el body.")
        if event_payload is None:
            raise HTTPException(status_code=400, detail="Falta 'payload' en el body.")

        logger.info(f"🔔 Procesando evento: topic={topic_str}")

        try:
            event_topic_enum = EventTopic(topic_str)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Topic inválido: '{topic_str}'")

        # Routing según el topic
        if event_topic_enum in [
            EventTopic.CRYPTO_PAYMENT,
            EventTopic.BUY_CRYPTO,
            EventTopic.SELL_CRYPTO
        ]:
            result = BlockchainTopicRouter.route(event_topic_enum, event_payload, db)
            return {
                "status": "success",
                "processed_id": result.id,
                "guild": "blockchain",
                "topic": event_topic_enum.value
            }

        elif event_topic_enum in [
            EventTopic.TENANT_CREADO,
            EventTopic.COMERCIO_CREADO,
            EventTopic.CATEGORIA_CREADA
        ]:
            result = MarketplaceTopicRouter.route(event_topic_enum, event_payload, db)
            return {
                "status": "success",
                "processed_id": (
                    getattr(result, 'tenant_id', None)
                    or getattr(result, 'comercio_id', None)
                    or getattr(result, 'categoria_id', None)
                ),
                "guild": "marketplace",
                "topic": event_topic_enum.value
            }

        elif event_topic_enum in [
            EventTopic.IVA_RESPUESTA
        ]:
            result = BackofficeTopicRouter.route(event_topic_enum, event_payload, db)
            return {
                "status": "success",
                "processed_id": result.processed_id,
                "guild": "backoffice",
                "topic": event_topic_enum.value,
                "details": {
                    "processed_orders": result.details.get('processed_count', 0),
                    "skipped_orders": result.details.get('skipped_count', 0),
                    "total_iva": result.details.get('total_iva_procesado', 0),
                    "orders": result.details.get('processed_orders', []),
                    "statistics": result.details.get('statistics', {})
                }
            }

        elif event_topic_enum in [
            EventTopic.PEDIDO_ACEPTADO,
            EventTopic.PEDIDO_ASIGNADO,
            EventTopic.PEDIDO_ENTREGADO,
            EventTopic.PEDIDO_ARRIBO,
            EventTopic.DELIVERY_NUEVOREPARTIDOR,
            EventTopic.PEDIDO_ENCAMINO,
            EventTopic.PEDIDO_CANCELADO
        ]:
            result = RepartidorTopicRouter.route(event_topic_enum, event_payload, db)
            return {
                "status": "success",
                "processed_id": getattr(result, 'id', None),
                "guild": "repartidor",
                "topic": event_topic_enum.value
            }

        elif event_topic_enum in BI_TOPICS:
            result = DashboardBiTopicRouter.route(event_topic_enum, event_payload, db)
            return {
                "status": "success",
                "processed_id": _get_bi_processed_id(result),
                "guild": "bi",
                "topic": event_topic_enum.value
            }

        elif event_topic_enum == EventTopic.BI_TEST:
            return event_payload

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported topic: {topic_str}. Please provide a valid topic."
            )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/callback")
async def webhook_challenge(
    request: Request
):
    """
    Verificación del webhook mediante parámetro ?challenge=...
    """
    challenge = request.query_params.get('challenge')
    logger.info(f"🛰️ Webhook challenge recibido: {challenge}")
    return PlainTextResponse(challenge or '')