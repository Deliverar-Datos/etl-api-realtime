from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import PedidoEnCamino

class PedidoEnCaminoProcessor:
    @staticmethod
    def process(db: Session, data: PedidoEnCamino):
        """Process pedido en camino event"""
        try:
            # Add your processing logic here
            print(f"Processing pedido en camino: {data}")
            return data
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing pedido en camino: {str(e)}")
