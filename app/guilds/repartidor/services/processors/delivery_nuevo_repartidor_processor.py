from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import DeliveryNuevoRepartidor

class DeliveryNuevoRepartidorProcessor:
    @staticmethod
    def process(db: Session, data: DeliveryNuevoRepartidor):
        """Process delivery nuevo repartidor event"""
        try:
            # Add your processing logic here
            print(f"Processing delivery nuevo repartidor: {data}")
            return data
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing delivery nuevo repartidor: {str(e)}")
