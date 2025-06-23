from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.events.schemas.base import EventTopic

class TenantData(BaseModel):
    tenant_id: int
    estado: str

class TenantCreateEvent(BaseModel):
    timestamp: datetime
    tenant: TenantData

class ComercioData(BaseModel):
    comercio_id: int
    tenant_id: int
    nombre: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    codigo_postal: Optional[str] = None

class ComercioCreateEvent(BaseModel):
    timestamp: datetime
    comercio: ComercioData

class CategoriaData(BaseModel):
    categoria_id: int
    tenant_id: int
    nombre: str

class CategoriaCreateEvent(BaseModel):
    timestamp: datetime
    categoria: CategoriaData
