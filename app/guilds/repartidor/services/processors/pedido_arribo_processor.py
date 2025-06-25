from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import PedidoArribo

class PedidoArriboProcessor:
    @staticmethod
    def process(db: Session, data: PedidoArribo):
        """Process pedido arribo event"""
        try:
            # Add your processing logic here
            print(f"Processing pedido arribo: {data}")
            return data
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing pedido arribo: {str(e)}")
