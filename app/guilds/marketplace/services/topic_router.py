from sqlalchemy.orm import Session
from app.events.schemas.base import EventTopic
from app.guilds.marketplace.schemas.events import TenantCreateEvent, ComercioCreateEvent, CategoriaCreateEvent
from .processors.create_tenant_processor import CreateTenantProcessor
from .processors.create_comercio import CreateComercioProcessor
from .processors.create_category import CreateCategoriaProcessor

class MarketplaceTopicRouter:
    @staticmethod
    def route(topic: str, payload: dict, db: Session):
        """Route marketplace events to appropriate processors"""
        try:
            if topic == "tenant.crear":
                print("Tenant Creation")
                data = TenantCreateEvent(**payload)
                return CreateTenantProcessor.process(db, data)
            elif topic == "comercio.crear":
                print("Comercio Creation")
                data = ComercioCreateEvent(**payload)
                return CreateComercioProcessor.process(db, data)
            elif topic == "categoria.crear":
                print("Categoria Creation")
                data = CategoriaCreateEvent(**payload)
                return CreateCategoriaProcessor.process(db, data)
            else:
                raise ValueError(f"Unsupported marketplace topic: {topic}")
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing {topic}: {str(e)}")
