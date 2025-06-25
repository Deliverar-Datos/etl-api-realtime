from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, Index, UniqueConstraint
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class PedidoIva(Base):
    """Tabla para almacenar pedidos con información de IVA"""
    __tablename__ = 'pedidos_iva'
    __table_args__ = (
        UniqueConstraint('pedido_id', name='uq_pedido_iva_pedido_id'),
        Index('ix_pedidos_iva_fecha_pedido', 'fecha_pedido'),
        Index('ix_pedidos_iva_monto_iva', 'monto_iva'),
        Index('ix_pedidos_iva_fecha_procesamiento', 'fecha_procesamiento'),
    )
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pedido_id = Column(String(100), nullable=False, unique=True, index=True, 
                      comment="ID único del pedido")
    fecha_pedido = Column(DateTime(timezone=True), nullable=False, 
                         comment="Fecha original del pedido")
    subtotal = Column(Numeric(12, 2), nullable=False, 
                     comment="Subtotal antes de IVA")
    monto_iva = Column(Numeric(12, 2), nullable=False, 
                      comment="Monto de IVA aplicado")
    total = Column(Numeric(12, 2), nullable=False, 
                  comment="Total incluyendo IVA")
    porcentaje_iva = Column(Numeric(5, 2), nullable=False, 
                           comment="Porcentaje de IVA calculado")
    fecha_procesamiento = Column(DateTime(timezone=True), 
                               server_default=func.now(), 
                               nullable=False,
                               comment="Fecha de procesamiento en ETL")
    
    def __repr__(self):
        return f"<PedidoIva(id={self.id}, pedido_id='{self.pedido_id}', total={self.total})>"
    
    @property
    def iva_calculado_correctamente(self) -> bool:
        """Verificar si el IVA fue calculado correctamente"""
        expected_total = self.subtotal + self.monto_iva
        return abs(float(self.total) - float(expected_total)) <= 0.01
    
    @property
    def resumen(self) -> dict:
        """Resumen del pedido para respuestas API"""
        return {
            "pedido_id": self.pedido_id,
            "fecha_pedido": self.fecha_pedido.isoformat(),
            "subtotal": float(self.subtotal),
            "monto_iva": float(self.monto_iva),
            "total": float(self.total),
            "porcentaje_iva": float(self.porcentaje_iva)
        }