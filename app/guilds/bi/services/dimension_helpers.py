from sqlalchemy.orm import Session
from app.guilds.bi.models.star_schema import (
    DimClient, DimDelivery, DimStatusOrder, DimStatusTransaction, DimDate, DimProduct,
    DimCurrency, DimMarketplace, DimCommerce, DimPromo
)
from datetime import datetime


def ensure_date(db: Session, date_value: datetime) -> DimDate:
    # Normalize to the start of the day to ensure one entry per calendar day
    normalized_date = date_value.replace(hour=0, minute=0, second=0, microsecond=0)
    
    existing = db.query(DimDate).filter(DimDate.date == normalized_date).first()
    if existing:
        return existing

    date_obj = DimDate(
        date=normalized_date,
        year=normalized_date.year,
        month=normalized_date.month,
        day=normalized_date.day
    )
    db.add(date_obj)
    return date_obj


def ensure_status_order(db: Session, status_str: str) -> DimStatusOrder:
    existing = db.query(DimStatusOrder).filter_by(status=status_str).first()
    if existing:
        return existing
    status = DimStatusOrder(status=status_str)
    db.add(status)
    return status


def ensure_status_transaction(db: Session, status_str: str) -> DimStatusTransaction:
    existing = db.query(DimStatusTransaction).filter_by(status=status_str).first()
    if existing:
        return existing
    status = DimStatusTransaction(status=status_str)
    db.add(status)
    return status


def ensure_currency(db: Session, description: str) -> DimCurrency:
    existing = db.query(DimCurrency).filter_by(description=description).first()
    if existing:
        return existing
    currency = DimCurrency(description=description)
    db.add(currency)
    return currency


def ensure_client(db: Session, client_id: int, name: str = "", surname: str = "", email: str = None, sign_up_date: datetime = None) -> DimClient:
    existing = db.query(DimClient).filter_by(client_id=client_id).first()
    if existing:
        return existing
    client = DimClient(
        client_id=client_id,
        name=name,
        surname=surname,
        email=email,
        sign_up_date=sign_up_date
    )
    db.add(client)
    return client


def ensure_delivery(db: Session, delivery_id: int, name: str = "", surname: str = "", email: str = None, sign_up_date: datetime = None, total_salary: float = 0.0) -> DimDelivery:
    existing = db.query(DimDelivery).filter_by(delivery_id=delivery_id).first()
    if existing:
        return existing
    delivery = DimDelivery(
        delivery_id=delivery_id,
        name=name,
        surname=surname,
        email=email,
        sign_up_date=sign_up_date,
        total_salary=total_salary
    )
    db.add(delivery)
    return delivery


def ensure_marketplace(db: Session, tenant_id: int, nombre: str = "", razon_social: str = "") -> DimMarketplace:
    existing = db.query(DimMarketplace).filter_by(tenant_id=tenant_id).first()
    if existing:
        return existing
    tenant = DimMarketplace(tenant_id=tenant_id, nombre=nombre, razon_social=razon_social)
    db.add(tenant)
    return tenant


def ensure_commerce(db: Session, commerce_id: int, name: str, post_code: int, tenant_id: int) -> DimCommerce:
    existing = db.query(DimCommerce).filter_by(commerce_id=commerce_id).first()
    if existing:
        return existing
    commerce = DimCommerce(commerce_id=commerce_id, name=name, post_code=post_code, tenant_id=tenant_id)
    db.add(commerce)
    return commerce


def ensure_promo(db: Session, promo_id: int, name: str, discount_type: str, discount_value: float, start_date_id: int, end_date_id: int) -> DimPromo:
    existing = db.query(DimPromo).filter_by(id=promo_id).first()
    if existing:
        return existing
    promo = DimPromo(
        id=promo_id,
        name=name,
        discount_type=discount_type,
        discount_value=discount_value,
        start_date_id=start_date_id,
        end_date_id=end_date_id
    )
    db.add(promo)
    return promo

def ensure_product(db: Session, product_id: int, name: str = "") -> DimProduct:
    existing = db.query(DimProduct).filter_by(id=product_id).first()
    if existing:
        return existing
    product = DimProduct(id=product_id, name=name)
    db.add(product)
    return product