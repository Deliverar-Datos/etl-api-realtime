from app.guilds.bi.schemas.events import PromoCommerceLinkedData
#from app.db import Base
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

# Tabla intermedia definida previamente
from app.guilds.bi.models.star_schema import dim_promo_commerce

class PromoCommerceLinkedProcessor:
    @staticmethod
    def process(db: Session, data: PromoCommerceLinkedData):
        try:
            # Check if the link already exists to ensure idempotency
            exists_stmt = select(dim_promo_commerce).where(
                dim_promo_commerce.c.promo_id == data.promoId,
                dim_promo_commerce.c.commerce_id == data.commerceId
            )
            if not db.execute(exists_stmt).first():
                stmt = insert(dim_promo_commerce).values(
                    promo_id=data.promoId,
                    commerce_id=data.commerceId
                )
                db.execute(stmt)
                db.commit()
            return {"promo_id": data.promoId, "commerce_id": data.commerceId}

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error linking promo to commerce: {str(e)}")
