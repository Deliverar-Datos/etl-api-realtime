from app.guilds.bi.schemas.events import CommerceRegisteredData
from sqlalchemy.orm import Session
from app.guilds.bi.services.dimension_helpers import ensure_commerce

class CommerceRegisteredProcessor:
    @staticmethod
    def process(db: Session, data: CommerceRegisteredData):
        try:
            commerce = ensure_commerce(
                db, data.commerceId, data.name, data.postCode, data.tenantId
            )
            db.commit()
            return commerce

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing commerce registration: {str(e)}")
