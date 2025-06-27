from app.events.schemas.base import EventTopic
from app.guilds.bi.schemas.events import ClientRegisteredData
from sqlalchemy.orm import Session
from app.guilds.bi.services.dimension_helpers import ensure_client

class ClientRegisteredProcessor:
    @staticmethod
    def process(db: Session, data: ClientRegisteredData):
        """Process client signed up events"""
        try:
            client = ensure_client(
                db, data.clientId, data.name, data.surname,
                data.email or '', data.signUpDate
            )
            db.commit()
            return client

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing client registration: {str(e)}")