from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List
from decimal import Decimal

class PedidoIva(BaseModel):
    """Modelo para un pedido individual con datos de IVA"""
    pedidoId: str = Field(..., min_length=1, max_length=100)
    fecha: datetime
    subtotal: float = Field(..., gt=0, description="Subtotal antes de IVA")
    montoIva: float = Field(..., ge=0, description="Monto de IVA aplicado")
    total: float = Field(..., gt=0, description="Total incluyendo IVA")
    
    @validator('total')
    def validar_total(cls, v, values):
        """Validar que total = subtotal + montoIva"""
        if 'subtotal' in values and 'montoIva' in values:
            expected_total = values['subtotal'] + values['montoIva']
            # Permitir pequeña diferencia por redondeo (0.01)
            if abs(v - expected_total) > 0.01:
                raise ValueError(
                    f"Total ({v}) debe ser igual a subtotal + montoIva ({expected_total})"
                )
        return v
    
    @property
    def porcentaje_iva(self) -> float:
        """Calcular porcentaje de IVA"""
        if self.subtotal > 0:
            return round((self.montoIva / self.subtotal) * 100, 2)
        return 0.0

class IvaRespuestaPayload(BaseModel):
    """Payload completo del evento iva.respuesta"""
    pedidos: List[PedidoIva] = Field(..., min_items=1, description="Lista de pedidos con IVA")
    
    @validator('pedidos')
    def validar_pedidos_unicos(cls, v):
        """Validar que no hay pedidoIds duplicados"""
        pedido_ids = [pedido.pedidoId for pedido in v]
        if len(pedido_ids) != len(set(pedido_ids)):
            raise ValueError("No se permiten pedidoIds duplicados en el mismo evento")
        return v
    
    @property
    def total_iva(self) -> float:
        """Total de IVA de todos los pedidos"""
        return sum(pedido.montoIva for pedido in self.pedidos)
    
    @property
    def total_general(self) -> float:
        """Total general de todos los pedidos"""
        return sum(pedido.total for pedido in self.pedidos)

class IvaRespuestaData(BaseModel):
    """Modelo principal para el evento iva.respuesta"""
    by: str = Field(default="Marketplace")
    topic: str = Field(default="iva.respuesta") 
    to: str = Field(default="BI")
    payload: IvaRespuestaPayload