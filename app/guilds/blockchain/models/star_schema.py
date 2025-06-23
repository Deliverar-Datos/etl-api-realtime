# app/models/star_schema.py
from sqlalchemy import (
    Column, Integer, String, Numeric, 
    Date, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class DimUser(Base):
    """User dimension table"""
    __tablename__ = 'dim_user'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    transactions_from = relationship(
        "FactTransaction", 
        foreign_keys="[FactTransaction.from_user_id]",
        back_populates="from_user"
    )
    transactions_to = relationship(
        "FactTransaction",
        foreign_keys="[FactTransaction.to_user_id]",
        back_populates="to_user"
    )
    transactions_email = relationship(
        "FactTransaction",
        foreign_keys="[FactTransaction.email_user_id]",
        back_populates="email_user"
    )

class DimStatus(Base):
    """Status dimension table"""
    __tablename__ = 'dim_status'
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(32), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relationships
    transactions = relationship("FactTransaction", back_populates="status")

class DimDate(Base):
    """Date dimension table"""
    __tablename__ = 'dim_date'
    __table_args__ = (
        UniqueConstraint('year', 'month', 'day', name='uq_date_components'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    weekday = Column(Integer, nullable=False)
    is_weekend = Column(Integer, default=0)
    
    # Relationships
    transactions = relationship("FactTransaction", back_populates="date")

class DimConcept(Base):
    """Concept dimension table"""
    __tablename__ = 'dim_concept'
    
    id = Column(Integer, primary_key=True, index=True)
    concept = Column(String(255), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=True)
    
    # Relationships
    transactions = relationship("FactTransaction", back_populates="concept")

class FactTransaction(Base):
    """Transaction fact table"""
    __tablename__ = 'facttransaction'
    __table_args__ = (
        UniqueConstraint('transaction_id', 'event_type', name='uq_transaction_event'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), index=True, nullable=False)
    event_type = Column(String(32), nullable=False)
    status_id = Column(Integer, ForeignKey('dim_status.id'), nullable=False)
    blockchain_tx_hash = Column(String(100), index=True)
    transaction_date = Column(DateTime(timezone=True), nullable=False)
    date_id = Column(Integer, ForeignKey('dim_date.id'), nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    concept_id = Column(Integer, ForeignKey('dim_concept.id'), nullable=False)
    from_user_id = Column(Integer, ForeignKey('dim_user.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('dim_user.id'), nullable=False)
    crypto_amount = Column(Numeric(20, 8))
    fiat_amount = Column(Numeric(20, 8))
    email_user_id = Column(Integer, ForeignKey('dim_user.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    status = relationship("DimStatus", back_populates="transactions")
    date = relationship("DimDate", back_populates="transactions")
    concept = relationship("DimConcept", back_populates="transactions")
    from_user = relationship(
        "DimUser", 
        foreign_keys=[from_user_id],
        back_populates="transactions_from"
    )
    to_user = relationship(
        "DimUser",
        foreign_keys=[to_user_id],
        back_populates="transactions_to"
    )
    email_user = relationship(
        "DimUser",
        foreign_keys=[email_user_id],
        back_populates="transactions_email"
    )

    @property
    def is_crypto(self):
        return self.event_type in ['buy_crypto', 'sell_crypto']