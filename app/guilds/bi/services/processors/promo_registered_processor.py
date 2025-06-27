from app.guilds.bi.schemas.events import FullPromoRegisteredData
from app.guilds.bi.models.star_schema import DimPromo, dim_promo_product
from sqlalchemy.orm import Session
from app.guilds.bi.services.dimension_helpers import ensure_date, ensure_promo, ensure_product
from sqlalchemy import insert, select

class PromoRegisteredProcessor:
    @staticmethod
    def process(db: Session, data: FullPromoRegisteredData):
        try:
            start_date_dim = ensure_date(db, data.fecha_inicio)
            end_date_dim = ensure_date(db, data.fecha_fin)

            promo = ensure_promo(
                db, data.promocion_id, data.nombre, data.tipo_descuento,
                data.valor_descuento, start_date_dim.id, end_date_dim.id
            )

            # Handle products affected by the promo
            for product_id in data.productos_afectados:
                # Ensure idempotency for product links
                exists_stmt = select(dim_promo_product).where(
                    dim_promo_product.c.promo_id == promo.id,
                    dim_promo_product.c.product_id == product_id
                )
                if not db.execute(exists_stmt).first():
                    stmt = insert(dim_promo_product).values(
                        promo_id=promo.id,
                        product_id=product_id
                    )
                    db.execute(stmt)

            db.commit()
            return promo

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing promo registration: {str(e)}")
