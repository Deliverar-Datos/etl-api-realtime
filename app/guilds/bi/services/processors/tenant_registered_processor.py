from app.guilds.bi.schemas.events import TenantRegisteredData, CommerceRegisteredData
from sqlalchemy.orm import Session
from app.guilds.bi.services.dimension_helpers import ensure_marketplace

class TenantRegisteredProcessor:
    @staticmethod
    def process(db: Session, data: TenantRegisteredData):
        try:
            tenant = ensure_marketplace(
                db, data.tenantId, data.nombre, data.razonSocial
            )
            db.commit()
            return tenant

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing tenant registration: {str(e)}")
