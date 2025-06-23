from sqlalchemy.orm import Session
from app.guilds.marketplace.models.tables import Comercio, Tenant
from app.guilds.marketplace.schemas.events import ComercioCreateEvent
from datetime import datetime

class CreateComercioProcessor:
    @staticmethod
    def process(db: Session, data: ComercioCreateEvent):
        """Process comercio creation events"""
        try:
            # Verify tenant exists
            tenant = db.query(Tenant).filter(Tenant.tenant_id == data.comercio.tenant_id).first()
            if not tenant:
                raise ValueError(f"Tenant with ID {data.comercio.tenant_id} does not exist")
            
            # Check if comercio already exists
            existing_comercio = db.query(Comercio).filter(Comercio.comercio_id == data.comercio.comercio_id).first()
            
            if existing_comercio:
                # Update existing comercio
                existing_comercio.tenant_id = data.comercio.tenant_id
                existing_comercio.nombre = data.comercio.nombre
                existing_comercio.lat = data.comercio.lat
                existing_comercio.lon = data.comercio.lon
                existing_comercio.calle = data.comercio.calle
                existing_comercio.numero = data.comercio.numero
                existing_comercio.ciudad = data.comercio.ciudad
                existing_comercio.provincia = data.comercio.provincia
                existing_comercio.codigo_postal = data.comercio.codigo_postal
                db.commit()
                return existing_comercio
            
            # Create new comercio with explicit creation date
            comercio = Comercio(
                comercio_id=data.comercio.comercio_id,
                tenant_id=data.comercio.tenant_id,
                nombre=data.comercio.nombre,
                lat=data.comercio.lat,
                lon=data.comercio.lon,
                calle=data.comercio.calle,
                numero=data.comercio.numero,
                ciudad=data.comercio.ciudad,
                provincia=data.comercio.provincia,
                codigo_postal=data.comercio.codigo_postal,
                fecha_creacion=data.timestamp
            )
            
            db.add(comercio)
            db.commit()
            return comercio
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing comercio creation: {str(e)}")
