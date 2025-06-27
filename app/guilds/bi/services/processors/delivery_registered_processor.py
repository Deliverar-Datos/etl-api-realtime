from app.guilds.bi.schemas.events import DeliveryRegisteredData
from sqlalchemy.orm import Session
from datetime import datetime
from app.guilds.bi.services.dimension_helpers import ensure_delivery

class DeliveryRegisteredProcessor:
    @staticmethod
    def process(db: Session, data: DeliveryRegisteredData):
        try:
            delivery = ensure_delivery(
                db, data.deliveryId, data.name, data.surname,
                data.email, data.signUpDate or datetime.utcnow(), data.totalSalary
            )
            db.commit()
            return delivery

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing delivery registration: {str(e)}")