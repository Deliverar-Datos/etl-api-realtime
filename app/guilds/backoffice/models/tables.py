from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.models.database import Base  # ← Usar la Base existente

class SolicitudIva(Base):
    """Table to track IVA calculation requests sent to Marketplace"""
    __tablename__ = 'solicitudes_iva'
    
    id = Column(Integer, primary_key=True, index=True)
    fecha_desde = Column(DateTime(timezone=True), nullable=False, index=True)
    fecha_hasta = Column(DateTime(timezone=True), nullable=False, index=True)
    fecha_solicitud = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now())
    estado = Column(String(50), default='ENVIADA', nullable=False)  # ENVIADA, PROCESADA, ERROR
    
    # Relationships
    pedidos_iva = relationship("PedidoIva", back_populates="solicitud")

class PedidoIva(Base):
    """Table to store orders with IVA calculations received from Marketplace"""
    __tablename__ = 'pedidos_iva'
    __table_args__ = (
        UniqueConstraint('pedido_id', 'fecha_procesamiento', name='uq_pedido_fecha'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(String(100), nullable=False, index=True)
    fecha_pedido = Column(DateTime(timezone=True), nullable=False, index=True)
    subtotal = Column(Float, nullable=False)
    monto_iva = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    
    # Tracking fields
    solicitud_id = Column(Integer, ForeignKey('solicitudes_iva.id'), nullable=True, index=True)
    fecha_procesamiento = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now())
    
    # Relationships
    solicitud = relationship("SolicitudIva", back_populates="pedidos_iva")
    
    @property
    def porcentaje_iva(self):
        """Calculate IVA percentage"""
        if self.subtotal > 0:
            return round((self.monto_iva / self.subtotal) * 100, 2)
        return 0.0