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
                existing_tenant.estado = data.tenant.estado
                db.commit()
                return existing_tenant
            
            # Create new tenant with explicit creation date
            tenant = Tenant(
                tenant_id=data.tenant.tenant_id,
                estado=data.tenant.estado,
                fecha_creacion=data.timestamp
            )
            
            db.add(tenant)
            db.commit()
            return tenant
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing tenant creation: {str(e)}")
