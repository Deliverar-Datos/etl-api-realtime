from sqlalchemy.orm import Session
from app.events.schemas.base import EventTopic
from app.guilds.marketplace.schemas.events import TenantCreadoPayload, ComercioCreadoPayload, CategoriaCreadaPayload
from .processors.create_tenant_processor import CreateTenantProcessor
from .processors.create_comercio import CreateComercioProcessor
from .processors.create_category import CreateCategoriaProcessor

class MarketplaceTopicRouter:
    @staticmethod
    def route(topic: str, payload: dict, db: Session):
        """Route marketplace events to appropriate processors"""
        try:
            if topic == "tenant.creado":
                print("Tenant Creation")
                data = TenantCreadoPayload(**payload)
                return CreateTenantProcessor.process(db, data)
            elif topic == "comercio.creado":
                print("Comercio Creation")
                data = ComercioCreadoPayload(**payload)
                return CreateComercioProcessor.process(db, data)
            elif topic == "categoria.creada":
                print("Categoria Creation")
                data = CategoriaCreadaPayload(**payload)
                return CreateCategoriaProcessor.process(db, data)
            else:
                raise ValueError(f"Unsupported marketplace topic: {topic}")
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing {topic}: {str(e)}")
