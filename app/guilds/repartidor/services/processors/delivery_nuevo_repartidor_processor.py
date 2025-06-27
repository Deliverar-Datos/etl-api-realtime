from sqlalchemy.orm import Session
from app.guilds.repartidor.schemas.events import DeliveryNuevoRepartidor
from app.guilds.repartidor.models.star_schema import DimRepartidor
from sqlalchemy.exc import SQLAlchemyError

def process(db: Session, data: DeliveryNuevoRepartidor):
    """Process delivery nuevo repartidor event"""
    try:
        # Verificar si el repartidor ya existe
        repartidor = db.query(DimRepartidor).filter(DimRepartidor.repartidor_id == data.repartidorId).first()
        if repartidor:
            # Actualizar datos existentes
            repartidor.nombre = data.nombre
            repartidor.apellido = data.apellido
            repartidor.email = data.email
            repartidor.telefono = data.telefono
        else:
            # Crear nuevo repartidor
            repartidor = DimRepartidor(
                repartidor_id=data.repartidorId,
                nombre=data.nombre,
                apellido=data.apellido,
                email=data.email,
                telefono=data.telefono
            )
            db.add(repartidor)
        db.commit()
        print(f"Repartidor guardado/actualizado: {data}")
        return data
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error processing delivery nuevo repartidor: {str(e)}")
