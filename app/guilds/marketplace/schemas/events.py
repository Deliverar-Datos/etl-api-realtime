from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.events.schemas.base import EventTopic

class UbicacionData(BaseModel):
    calle: Optional[str] = None
    numero: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    codigo_postal: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class TenantData(BaseModel):
    tenant_id: int
    nombre: str
    razon_social: Optional[str] = None
    ubicacion: Optional[UbicacionData] = None
    cuenta_bancaria: Optional[str] = None
    estado: str

class TenantCreateEvent(BaseModel):
    tenant: TenantData
    timestamp: datetime

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
    comercio: ComercioData
    timestamp: datetime

class CategoriaData(BaseModel):
    categoria_id: int
    tenant_id: int
    nombre: str

class CategoriaCreateEvent(BaseModel):
    categoria: CategoriaData
    timestamp: datetime
