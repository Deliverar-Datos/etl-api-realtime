from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.events.schemas.base import EventTopic
from app.models.database import create_tables, get_db
from app.guilds.blockchain.services.topic_router import BlockchainTopicRouter
from app.guilds.marketplace.services.topic_router import MarketplaceTopicRouter

from app.guilds.repartidor.services.topic_router import RepartidorTopicRouter

from app.guilds.backoffice.services.topic_router import BackofficeTopicRouter

import logging
from fastapi.responses import PlainTextResponse
import pdb


logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/callback")
async def handle_event(
    raw_request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle events from different guilds based on topic.
    
    Topic-based routing:
    - crypto.payment, buy.crypto, sell.crypto -> blockchain guild
    - tenant.creado, comercio.creado, categoria.creada -> marketplace guild
    - pedido.aceptado, pedido.asignado, pedido.entregado, pedido.arribo, delivery.nuevoRepartidor, pedido.enCamino, pedido.cancelado -> repartidor guild
    - iva.respuesta -> backoffice guild
    """
    try:
        print(f"Raw request headers: {dict(raw_request.headers)}")
        print(f"Raw request query params: {dict(raw_request.query_params)}")
        
        # Get topic from x-topic header
        topic = raw_request.headers.get('x-topic')
        print(f"Topic from header: {topic}")

        payload = await raw_request.json()
        
        if not topic:
            raise HTTPException(status_code=400, detail="Missing x-topic header")
        
        create_tables()
        print("Tables created")
        logger.info(f"Processing event: topic={topic}")

        # Route based on topic to determine guild
        if topic in [EventTopic.CRYPTO_PAYMENT, EventTopic.BUY_CRYPTO, EventTopic.SELL_CRYPTO]:
            result = BlockchainTopicRouter.route(topic, payload, db)
            return {
                "status": "success", 
                "processed_id": result.id,
                "guild": "blockchain",
                "topic": topic
            }
        elif topic in [EventTopic.TENANT_CREADO, EventTopic.COMERCIO_CREADO, EventTopic.CATEGORIA_CREADA]:
            result = MarketplaceTopicRouter.route(topic, payload, db)
            return {
                "status": "success", 
                "processed_id": result.tenant_id if hasattr(result, 'tenant_id') else result.comercio_id if hasattr(result, 'comercio_id') else result.categoria_id,
                "guild": "marketplace",
                "topic": topic
            }
        elif topic in [EventTopic.IVA_RESPUESTA]:
            result = BackofficeTopicRouter.route(topic, payload, db)
            return {
                "status": "success", 
                "processed_id": result.processed_id,
                "guild": "backoffice",
                "topic": topic,
                "details": {
                    "processed_orders": result.details.get('processed_count', 0),
                    "skipped_orders": result.details.get('skipped_count', 0),
                    "total_iva": result.details.get('total_iva_procesado', 0),
                    "orders": result.details.get('processed_orders', []),
                    "statistics": result.details.get('statistics', {})
                }
            }
        elif topic in [EventTopic.BI_TEST]:
            return payload
        elif topic in [
            EventTopic.PEDIDO_ACEPTADO,
            EventTopic.PEDIDO_ASIGNADO,
            EventTopic.PEDIDO_ENTREGADO,
            EventTopic.PEDIDO_ARRIBO,
            EventTopic.DELIVERY_NUEVOREPARTIDOR,
            EventTopic.PEDIDO_ENCAMINO,
            EventTopic.PEDIDO_CANCELADO,
        ]:
            result = RepartidorTopicRouter.route(topic, payload, db)
            return {
                "status": "success",
                "processed_id": result.id if hasattr(result, 'id') else None,
                "guild": "repartidor",
                "topic": topic,
            }
        else:
            return payload
            
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.get("/callback")
async def handle_event(
    request: Request
):
    """
    Verificación de webhook por parte de deliver.ar
    """
    challenge = request.query_params.get('challenge')
    logger.info(f"🔍 Deliver.ar challenge verification: {challenge}")
    
    # Responder el challenge para confirmar el webhook
    return PlainTextResponse(challenge or '')