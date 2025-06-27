from app.guilds.bi.schemas.events import OrderRegisteredData
from app.guilds.bi.models.star_schema import DimOrder, DimStatusOrder, DimDate
from sqlalchemy.orm import Session
from datetime import datetime # Keep datetime import if needed for default values or type hints
from app.guilds.bi.services.dimension_helpers import ensure_status_order, ensure_date

class OrderRegistredProcessor:
    @staticmethod
    def process(db: Session, data: OrderRegisteredData):
        try:
            status_before = ensure_status_order(db, data.statusBefore)
            status_after = ensure_status_order(db, data.statusAfter)
            date_dim = ensure_date(db, data.date)

            order = db.query(DimOrder).filter_by(order_id=data.orderId).first()
            if not order:
                order = DimOrder(
                    order_id=data.orderId,
                    client_id=data.clientId,
                    delivery_id=data.deliveryId,
                    status_before_id=status_before.id,
                    status_after_id=status_after.id,   
                    date_id=date_dim.id,   
                    start_delivery=data.startDelivery,
                    end_delivery=data.endDelivery,
                    comission=data.comission,
                    promo_id=data.promoId
                )
                db.add(order)

            db.commit()
            return order

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing order registration: {str(e)}")
