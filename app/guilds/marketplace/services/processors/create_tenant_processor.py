from sqlalchemy.orm import Session
from app.guilds.marketplace.models.tables import Tenant
from app.guilds.marketplace.schemas.events import TenantCreateEvent
from datetime import datetime

class CreateTenantProcessor:
    @staticmethod
    def process(db: Session, data: TenantCreateEvent):
        """Process tenant creation events"""
        try:
            # Check if tenant already exists
            existing_tenant = db.query(Tenant).filter(Tenant.tenant_id == data.tenant.tenant_id).first()
            
            if existing_tenant:
                # Update existing tenant
                existing_tenant.nombre = data.tenant.nombre
                existing_tenant.razon_social = data.tenant.razon_social
                existing_tenant.cuenta_bancaria = data.tenant.cuenta_bancaria
                existing_tenant.estado = data.tenant.estado
                
                # Update location if provided
                if data.tenant.ubicacion:
                    existing_tenant.calle = data.tenant.ubicacion.calle
                    existing_tenant.numero = data.tenant.ubicacion.numero
                    existing_tenant.ciudad = data.tenant.ubicacion.ciudad
                    existing_tenant.provincia = data.tenant.ubicacion.provincia
                    existing_tenant.codigo_postal = data.tenant.ubicacion.codigo_postal
                    existing_tenant.lat = data.tenant.ubicacion.lat
                    existing_tenant.lon = data.tenant.ubicacion.lon
                
                db.commit()
                return existing_tenant
            
            # Create new tenant with explicit creation date
            tenant = Tenant(
                tenant_id=data.tenant.tenant_id,
                nombre=data.tenant.nombre,
                razon_social=data.tenant.razon_social,
                cuenta_bancaria=data.tenant.cuenta_bancaria,
                estado=data.tenant.estado,
                fecha_creacion=data.timestamp
            )
            
            # Set location if provided
            if data.tenant.ubicacion:
                tenant.calle = data.tenant.ubicacion.calle
                tenant.numero = data.tenant.ubicacion.numero
                tenant.ciudad = data.tenant.ubicacion.ciudad
                tenant.provincia = data.tenant.ubicacion.provincia
                tenant.codigo_postal = data.tenant.ubicacion.codigo_postal
                tenant.lat = data.tenant.ubicacion.lat
                tenant.lon = data.tenant.ubicacion.lon
            
            db.add(tenant)
            db.commit()
            return tenant
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing tenant creation: {str(e)}")
