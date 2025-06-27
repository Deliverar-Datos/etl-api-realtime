from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PedidoAceptado(BaseModel):
    pedidoId: str
    estado: str

class PedidoAsignado(BaseModel):
    pedidoId: str
    estado: str
    repartidor: dict

class PedidoEntregado(BaseModel):
    pedidoId: str
    estado: str

class PedidoArribo(BaseModel):
    pedidoId: str
    estado: str

class DeliveryNuevoRepartidor(BaseModel):
    repartidorId: int
    nombre: str
    apellido: str
    email: str
    telefono: str

class PedidoEnCamino(BaseModel):
    pedidoId: str
    estado: str

class PedidoCancelado(BaseModel):
    pedidoId: str
    estado: str
