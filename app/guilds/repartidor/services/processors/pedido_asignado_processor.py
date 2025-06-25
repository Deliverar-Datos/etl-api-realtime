from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import PedidoAsignado

class PedidoAsignadoProcessor:
    @staticmethod
    def process(db: Session, data: PedidoAsignado):
        """Process pedido asignado event"""
        try:
            # Add your processing logic here
            print(f"Processing pedido asignado: {data}")
            return data
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing pedido asignado: {str(e)}")
