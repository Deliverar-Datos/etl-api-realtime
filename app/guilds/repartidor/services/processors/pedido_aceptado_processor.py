from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import PedidoAceptado

class PedidoAceptadoProcessor:
    @staticmethod
    def process(db: Session, data: PedidoAceptado):
        """Process pedido aceptado event"""
        try:
            # Add your processing logic here
            print(f"Processing pedido aceptado: {data}")
            return data
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing pedido aceptado: {str(e)}")
