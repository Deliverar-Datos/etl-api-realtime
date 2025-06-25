from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import PedidoEntregado

class PedidoEntregadoProcessor:
    @staticmethod
    def process(db: Session, data: PedidoEntregado):
        """Process pedido entregado event"""
        try:
            # Add your processing logic here
            print(f"Processing pedido entregado: {data}")
            return data
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing pedido entregado: {str(e)}")
