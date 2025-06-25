from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.events.schemas.base import CallbackRequest, EventTopic
from app.models.database import create_tables, get_db
from app.guilds.blockchain.services.topic_router import BlockchainTopicRouter
from app.guilds.marketplace.services.topic_router import MarketplaceTopicRouter
import logging
from fastapi.responses import PlainTextResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/callback")
async def handle_event(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle events from different guilds based on topic.
    
    Topic-based routing:
    - crypto.payment, buy.crypto, sell.crypto -> blockchain guild
    - tenant.creado, comercio.creado, categoria.creada -> marketplace guild
    """
    try:
        print(request)
        create_tables()
        print("Tables created")
        logger.info(f"Processing event: topic={request.topic}")

        
        # Route based on topic to determine guild
        if request.topic in [EventTopic.CRYPTO_PAYMENT, EventTopic.BUY_CRYPTO, EventTopic.SELL_CRYPTO]:
            result = BlockchainTopicRouter.route(request.topic, request.payload, db)
            return {
                "status": "success", 
                "processed_id": result.id,
                "guild": "blockchain",
                "topic": request.topic
            }
        elif request.topic in [EventTopic.TENANT_CREADO, EventTopic.COMERCIO_CREADO, EventTopic.CATEGORIA_CREADA]:
            result = MarketplaceTopicRouter.route(request.topic, request.payload, db)
            return {
                "status": "success", 
                "processed_id": result.tenant_id if hasattr(result, 'tenant_id') else result.comercio_id if hasattr(result, 'comercio_id') else result.categoria_id,
                "guild": "marketplace",
                "topic": request.topic
            }
        elif request.topic in [EventTopic.BI_TEST]:
            return request
        else:
            return request
            
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
