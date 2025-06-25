from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text, TIMESTAMP
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Tenant(Base):
    """Tenant table"""
    __tablename__ = 'tenants'
    
    tenant_id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    razon_social = Column(String(255))
    calle = Column(String(255))
    numero = Column(String(50))
    ciudad = Column(String(255))
    provincia = Column(String(255))
    codigo_postal = Column(String(20))
    lat = Column(Float)
    lon = Column(Float)
    cuenta_bancaria = Column(String(255))
    estado = Column(String(50))
    fecha_creacion = Column(TIMESTAMP)
    
    # Relationships
    comercios = relationship("Comercio", back_populates="tenant")
    categorias = relationship("Categoria", back_populates="tenant")

class Comercio(Base):
    """Comercio table"""
    __tablename__ = 'comercios'
    
    comercio_id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), nullable=False)
    nombre = Column(String(255), nullable=False)
    lat = Column(Float)
    lon = Column(Float)
    calle = Column(String(255))
    numero = Column(String(50))
    ciudad = Column(String(255))
    provincia = Column(String(255))
    codigo_postal = Column(String(20))
    fecha_creacion = Column(TIMESTAMP)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="comercios")

class Categoria(Base):
    """Categoria table"""
    __tablename__ = 'categorias'
    
    categoria_id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), nullable=False)
    nombre = Column(String(255), nullable=False)
    fecha_creacion = Column(TIMESTAMP)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="categorias")
