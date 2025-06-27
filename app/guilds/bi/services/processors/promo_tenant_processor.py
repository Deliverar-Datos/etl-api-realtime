from app.guilds.bi.schemas.events import PromoTenantLinkedData
#from app.db import Base
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

# Tabla intermedia definida previamente
from app.guilds.bi.models.star_schema import dim_promo_tenant

class PromoTenantLinkedProcessor:
    @staticmethod
    def process(db: Session, data: PromoTenantLinkedData):
        try:
            # Check if the link already exists to ensure idempotency
            exists_stmt = select(dim_promo_tenant).where(
                dim_promo_tenant.c.promo_id == data.promoId,
                dim_promo_tenant.c.tenant_id == data.tenantId
            )
            if not db.execute(exists_stmt).first():
                stmt = insert(dim_promo_tenant).values(
                    promo_id=data.promoId,
                    tenant_id=data.tenantId
                )
                db.execute(stmt)
                db.commit()
            return {"promo_id": data.promoId, "tenant_id": data.tenantId}

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error linking promo to tenant: {str(e)}")
