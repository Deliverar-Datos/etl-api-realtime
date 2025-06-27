# app/models/star_schema.py
from sqlalchemy import (
    Column, Integer, Float, String, Numeric, 
    DateTime, ForeignKey, Table, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.database import Base

# --- Asociación ---
dim_promo_commerce = Table(
    "bi_dim_promo_commerce", Base.metadata,
    Column("promo_id", Integer, ForeignKey("bi_dim_promo.id"), primary_key=True),
    Column("commerce_id", Integer, ForeignKey("bi_dim_commerce.commerce_id"), primary_key=True)
)

dim_promo_tenant = Table(
    "bi_dim_promo_tenant", Base.metadata,
    Column("promo_id", Integer, ForeignKey("bi_dim_promo.id"), primary_key=True),
    Column("tenant_id", Integer, ForeignKey("bi_dim_marketplace.tenant_id"), primary_key=True)
)

dim_promo_product = Table(
    "bi_dim_promo_product", Base.metadata,
    Column("promo_id", Integer, ForeignKey("bi_dim_promo.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("bi_dim_product.id"), primary_key=True)
)


# --- Dimensiones ---
class DimDate(Base):
    __tablename__ = "bi_dim_date"
    __table_args__ = (UniqueConstraint('date', name='uq_date_components'),)

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)

    start_promos = relationship("DimPromo", foreign_keys="[DimPromo.start_date_id]", back_populates="start_date_dim")
    #reports = relationship("DashboardBiReports", back_populates="date_dim")
    end_promos = relationship("DimPromo", foreign_keys="[DimPromo.end_date_id]", back_populates="end_date_dim")
    orders = relationship("DimOrder", back_populates="date_dim") # Mantener para la FK en DimOrder
    transactions = relationship("DimBlockchainTransactions", back_populates="date_dim") # Mantener para la FK en DimBlockchainTransactions

class DimClient(Base):
    __tablename__ = "bi_dim_clients"

    client_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    email = Column(String(40), nullable=True)
    sign_up_date = Column(DateTime, nullable=False)

    orders = relationship("DimOrder", back_populates="client_dim")
    transactions = relationship("DimBlockchainTransactions", back_populates="client_dim")

class DimDelivery(Base):
    __tablename__ = "bi_dim_delivery"

    delivery_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    email = Column(String(40), nullable=True)
    sign_up_date = Column(DateTime, nullable=False)
    total_salary = Column(Float, nullable=False)

    orders = relationship("DimOrder", back_populates="delivery_dim")

class DimCurrency(Base):
    __tablename__ = "bi_dim_currency"

    currency_id = Column(Integer, primary_key=True, index=True)
    description = Column(String(20), nullable=False)

    transactions = relationship("DimBlockchainTransactions", back_populates="currency_dim")

class DimStatusOrder(Base):
    __tablename__ = "bi_dim_status_order"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), unique=True, nullable=False)

    status_before_orders = relationship("DimOrder", foreign_keys='DimOrder.status_before_id', back_populates="status_before_dim")
    status_after_orders = relationship("DimOrder", foreign_keys='DimOrder.status_after_id', back_populates="status_after_dim")

class DimStatusTransaction(Base):
    __tablename__ = "bi_dim_status_transaction"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), unique=True, nullable=False)

    transactions = relationship("DimBlockchainTransactions", back_populates="status_dim")

class DimMarketplace(Base):
    __tablename__ = "bi_dim_marketplace"

    tenant_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    razon_social = Column(String(50), nullable=False)

    commerces = relationship("DimCommerce", back_populates="tenant")
    promos = relationship("DimPromo", secondary=dim_promo_tenant, back_populates="tenants")

class DimCommerce(Base):
    __tablename__ = "bi_dim_commerce"

    commerce_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    post_code = Column(Integer, nullable=False)
    tenant_id = Column(Integer, ForeignKey("bi_dim_marketplace.tenant_id"), nullable=False)

    tenant = relationship("DimMarketplace", back_populates="commerces")
    promos = relationship("DimPromo", secondary=dim_promo_commerce, back_populates="commerces")

class DimPromo(Base):
    __tablename__ = "bi_dim_promo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    discount_type = Column(String(20), nullable=False)
    discount_value = Column(Float, nullable=False)
    # product_id is now handled via dim_promo_product association table
    start_date_id = Column(Integer, ForeignKey("bi_dim_date.id"), nullable=False)
    end_date_id = Column(Integer, ForeignKey("bi_dim_date.id"), nullable=False)
    orders = relationship("DimOrder", back_populates="promo_dim")

    commerces = relationship("DimCommerce", secondary=dim_promo_commerce, back_populates="promos")
    tenants = relationship("DimMarketplace", secondary=dim_promo_tenant, back_populates="promos")
    products = relationship("DimProduct", secondary=dim_promo_product, back_populates="promos") # New relationship
    start_date_dim = relationship("DimDate", foreign_keys=[start_date_id], back_populates="start_promos")
    end_date_dim = relationship("DimDate", foreign_keys=[end_date_id], back_populates="end_promos")

# --- Hechos ---
class DimOrder(Base):
    __tablename__ = "bi_dim_order"

    order_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("bi_dim_clients.client_id"))
    delivery_id = Column(Integer, ForeignKey("bi_dim_delivery.delivery_id"))
    status_before_id = Column(Integer, ForeignKey("bi_dim_status_order.id"), nullable=False)
    status_after_id = Column(Integer, ForeignKey("bi_dim_status_order.id"), nullable=False)
    date_id = Column(Integer, ForeignKey("bi_dim_date.id"), nullable=False)
    promo_id = Column(Integer, ForeignKey("bi_dim_promo.id"), nullable=True) # <-- AÑADIDO
    start_delivery = Column(DateTime)
    end_delivery = Column(DateTime)
    comission = Column(Float, nullable=False)

    date_dim = relationship("DimDate", back_populates="orders")
    promo_dim = relationship("DimPromo", back_populates="orders") # <-- AÑADIDO
    client_dim = relationship("DimClient", back_populates="orders")
    delivery_dim = relationship("DimDelivery", back_populates="orders")
    status_before_dim = relationship("DimStatusOrder", foreign_keys=[status_before_id], back_populates="status_before_orders")
    status_after_dim = relationship("DimStatusOrder", foreign_keys=[status_after_id], back_populates="status_after_orders")

class DimBlockchainTransactions(Base):
    __tablename__ = "bi_dim_blockchain_transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    date_id = Column(Integer, ForeignKey("bi_dim_date.id"), nullable=False) # Changed to nullable=False
    client_id = Column(Integer, ForeignKey("bi_dim_clients.client_id"), nullable=True) # Keep as nullable=True
    amount = Column(Float, nullable=False) # Changed to nullable=False
    currency_id = Column(Integer, ForeignKey("bi_dim_currency.currency_id"), nullable=False) # Changed to nullable=False
    concept = Column(String, nullable=False) # Changed to nullable=False
    status_id = Column(Integer, ForeignKey("bi_dim_status_transaction.id"), nullable=False) # Changed to nullable=False

    currency_dim = relationship("DimCurrency", back_populates="transactions")
    status_dim = relationship("DimStatusTransaction", back_populates="transactions")
    date_dim = relationship("DimDate", back_populates="transactions")
    client_dim = relationship("DimClient", back_populates="transactions")

class DimProduct(Base): # New Dimension for Products
    __tablename__ = "bi_dim_product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    promos = relationship("DimPromo", secondary=dim_promo_product, back_populates="products")
