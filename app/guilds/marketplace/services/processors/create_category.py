from sqlalchemy.orm import Session
from app.guilds.marketplace.models.tables import Categoria, Tenant
from app.guilds.marketplace.schemas.events import CategoriaCreadaPayload
from datetime import datetime

class CreateCategoriaProcessor:
    @staticmethod
    def process(db: Session, data: CategoriaCreadaPayload):
        """Process categoria creation events"""
        try:
            # Verify tenant exists
            tenant = db.query(Tenant).filter(Tenant.tenant_id == data.categoria.tenant_id).first()
            if not tenant:
                raise ValueError(f"Tenant with ID {data.categoria.tenant_id} does not exist")
            
            # Check if categoria already exists
            existing_categoria = db.query(Categoria).filter(Categoria.categoria_id == data.categoria.categoria_id).first()
            
            if existing_categoria:
                # Update existing categoria
                existing_categoria.tenant_id = data.categoria.tenant_id
                existing_categoria.nombre = data.categoria.nombre
                db.commit()
                return existing_categoria
            
            # Create new categoria with explicit creation date
            categoria = Categoria(
                categoria_id=data.categoria.categoria_id,
                tenant_id=data.categoria.tenant_id,
                nombre=data.categoria.nombre,
                fecha_creacion=data.timestamp
            )
            
            db.add(categoria)
            db.commit()
            return categoria
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing categoria creation: {str(e)}")
