from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Tenant(Base):
    """Tenant table"""
    __tablename__ = 'tenants'
    
    tenant_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    razon_social = Column(Text, nullable=True)
    calle = Column(Text, nullable=True)
    numero = Column(Text, nullable=True)
    ciudad = Column(Text, nullable=True)
    provincia = Column(Text, nullable=True)
    codigo_postal = Column(Text, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    cuenta_bancaria = Column(Text, nullable=True)
    estado = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now())
    
    # Relationships
    comercios = relationship("Comercio", back_populates="tenant")
    categorias = relationship("Categoria", back_populates="tenant")

class Comercio(Base):
    """Comercio table"""
    __tablename__ = 'comercios'
    
    comercio_id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), nullable=False)
    nombre = Column(Text, nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    calle = Column(Text, nullable=True)
    numero = Column(Text, nullable=True)
    ciudad = Column(Text, nullable=True)
    provincia = Column(Text, nullable=True)
    codigo_postal = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="comercios")

class Categoria(Base):
    """Categoria table"""
    __tablename__ = 'categorias'
    
    categoria_id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), nullable=False)
    nombre = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="categorias")
