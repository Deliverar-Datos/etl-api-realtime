from sqlalchemy.orm import Session
from app.events.schemas.base import EventTopic
from app.guilds.bi.schemas.events import (
    OrderRegisteredData,
    OrderStatusUpdatedData,
    ClientRegisteredData,
    DeliveryRegisteredData,
    FullPromoRegisteredData,
    PromoTenantLinkedData,
    PromoCommerceLinkedData,
    BlockchainTransactionRegisteredData,
    TenantRegisteredData,
    CommerceRegisteredData
)
from .processors.order_registered_processor import OrderRegistredProcessor
# from .processors.order_status_updated_processor import OrderStatusUpdatedProcessor # To be implemented
from .processors.client_registered_processor import ClientRegisteredProcessor
from .processors.delivery_registered_processor import DeliveryRegisteredProcessor
from .processors.promo_registered_processor import PromoRegisteredProcessor
from .processors.commerce_registered_processor import CommerceRegisteredProcessor
from .processors.tenant_registered_processor import TenantRegisteredProcessor
from .processors.promo_tenant_processor import PromoTenantLinkedProcessor
from .processors.promo_commerce_procesor import PromoCommerceLinkedProcessor
from .processors.transaction_registred_processor import BlockchainTransactionRegisteredProcessor


EVENT_MAP = {
    EventTopic.ORDEN_REGISTRADA: (OrderRegisteredData, OrderRegistredProcessor),
    # EventTopic.ORDEN_ESTADO_ACTUALIZADO: (OrderStatusUpdatedData, OrderStatusUpdatedProcessor),
    EventTopic.CLIENT_REGISTRADO: (ClientRegisteredData, ClientRegisteredProcessor),
    EventTopic.DELIVERY_REGISTRADO: (DeliveryRegisteredData, DeliveryRegisteredProcessor),
    EventTopic.PROMO_REGISTRADA: (FullPromoRegisteredData, PromoRegisteredProcessor),
    EventTopic.PROMO_TENANT_ASOCIADA: (PromoTenantLinkedData, PromoTenantLinkedProcessor),
    EventTopic.PROMO_COMERCIO_ASOCIADA: (PromoCommerceLinkedData, PromoCommerceLinkedProcessor),
    EventTopic.COMERCIO_CREADO: (CommerceRegisteredData, CommerceRegisteredProcessor),
    EventTopic.TENANT_CREADO: (TenantRegisteredData, TenantRegisteredProcessor),
    EventTopic.TRANSACCION_BLOCKCHAIN_REGISTRADA: (BlockchainTransactionRegisteredData, BlockchainTransactionRegisteredProcessor),
}

class DashboardBiTopicRouter:
    @staticmethod
    def route(topic: str, payload: dict, db: Session):
        """Route DashboardBI events to appropriate processors"""
        try:
            handler = EVENT_MAP.get(topic)
            if not handler:
                raise ValueError(f"Unsupported dashboardbi topic: {topic}")
            
            schema, processor = handler
            data = schema(**payload)
            return processor.process(db, data)
        
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing {topic}: {str(e)}")
