from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

class IvaPedidoData(BaseModel):
    """Schema for IVA request data"""
    fechaDesde: datetime = Field(..., description="Start date for IVA calculation period")
    fechaHasta: datetime = Field(..., description="End date for IVA calculation period")

class PedidoIvaData(BaseModel):
    """Schema for individual order with IVA data"""
    pedidoId: str = Field(..., max_length=100, description="Order ID")
    fecha: datetime = Field(..., description="Order date")
    subtotal: float = Field(..., ge=0, description="Subtotal amount before taxes")
    montoIva: float = Field(..., ge=0, description="IVA amount")
    total: float = Field(..., ge=0, description="Total amount including IVA")

class IvaRespuestaData(BaseModel):
    """Schema for IVA response data containing multiple orders"""
    pedidos: List[PedidoIvaData] = Field(..., description="List of orders with IVA calculations")