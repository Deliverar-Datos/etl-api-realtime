from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.events.schemas.base import CallbackRequest, EventTopic
from app.models.database import create_tables, get_db
from app.guilds.blockchain.services.topic_router import BlockchainTopicRouter
from app.guilds.marketplace.services.topic_router import MarketplaceTopicRouter
from app.guilds.backoffice.services.topic_router import BackofficeTopicRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/callback")
async def handle_event(
    request: CallbackRequest,
    db: Session = Depends(get_db)
):
    """
    Handle events from different guilds based on topic.
    
    Topic-based routing:
    - crypto.payment, buy.crypto, sell.crypto -> blockchain guild
    - tenant.creado, comercio.creado, categoria.creada -> marketplace guild
    - iva.pedido, iva.respuesta -> backoffice guild
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
        elif request.topic in [EventTopic.IVA_PEDIDO, EventTopic.IVA_RESPUESTA]:
            result = BackofficeTopicRouter.route(request.topic, request.payload, db)
            
            # Handle different response types for backoffice
            if request.topic == EventTopic.IVA_PEDIDO:
                processed_id = result.id
            else:  # IVA_RESPUESTA
                processed_id = result.get("processed_orders", 0)
            
            return {
                "status": "success",
                "processed_id": processed_id,
                "guild": "backoffice",
                "topic": request.topic,
                "details": result if isinstance(result, dict) else None
            }      
        
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported topic: {request.topic}. Supported topics: crypto.payment, buy.crypto, sell.crypto, tenant.creado, comercio.creado, categoria.creada, iva.pedido, iva.respuesta"
            )
            
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")