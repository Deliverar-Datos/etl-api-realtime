from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Dimension Tables
class DimUser(Base):
    __tablename__ = "dim_user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), unique=True, index=True, nullable=False)
    
    # Relationships
    from_transactions = relationship("FactTransaction", foreign_keys="FactTransaction.from_user_id")
    to_transactions = relationship("FactTransaction", foreign_keys="FactTransaction.to_user_id")
    email_transactions = relationship("FactTransaction", foreign_keys="FactTransaction.email_user_id")

class DimStatus(Base):
    __tablename__ = "dim_status"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    transactions = relationship("FactTransaction", back_populates="status")

class DimDate(Base):
    __tablename__ = "dim_date"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    
    # Relationships
    transactions = relationship("FactTransaction", back_populates="date_dim")

class DimConcept(Base):
    __tablename__ = "dim_concept"
    
    id = Column(Integer, primary_key=True, index=True)
    concept = Column(String(100), unique=True, nullable=False)
    
    # Relationships
    transactions = relationship("FactTransaction", back_populates="concept")

# Fact Table
class FactTransaction(Base):
    __tablename__ = "fact_transaction"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, nullable=False, index=True)
    event_type = Column(String(50), nullable=False)  # payment, buy_crypto, sell_crypto
    
    # Foreign Keys
    status_id = Column(Integer, ForeignKey("dim_status.id"), nullable=False)
    date_id = Column(Integer, ForeignKey("dim_date.id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("dim_user.id"), nullable=True)
    to_user_id = Column(Integer, ForeignKey("dim_user.id"), nullable=True)
    email_user_id = Column(Integer, ForeignKey("dim_user.id"), nullable=True)
    concept_id = Column(Integer, ForeignKey("dim_concept.id"), nullable=True)
    
    # Transaction Data
    blockchain_tx_hash = Column(String(255), nullable=True)
    transaction_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=True)  # For payments
    fiat_amount = Column(Float, nullable=True)  # For buy/sell crypto
    
    # Metadata
    
    # Relationships
    status = relationship("DimStatus", back_populates="transactions")
    date_dim = relationship("DimDate", back_populates="transactions")
    concept = relationship("DimConcept", back_populates="transactions")
