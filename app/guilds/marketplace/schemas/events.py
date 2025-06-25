from pydantic import BaseModel
from typing import Optional

class Ubicacion(BaseModel):
    calle: str
    numero: str
    ciudad: str
    provincia: str
    codigo_postal: str
    lat: float
    lon: float

class TenantData(BaseModel):
    tenant_id: int
    nombre: str
    razon_social: Optional[str]
    ubicacion: Ubicacion
    cuenta_bancaria: Optional[str]
    estado: Optional[str]

class ComercioData(BaseModel):
    comercio_id: int
    tenant_id: int
    nombre: str
    lat: float
    lon: float
    calle: str
    numero: str
    ciudad: str
    provincia: str
    codigo_postal: str

class CategoriaData(BaseModel):
    categoria_id: int
    tenant_id: int
    nombre: str

class TenantCreadoPayload(BaseModel):
    tenant: TenantData
    timestamp: str

class ComercioCreadoPayload(BaseModel):
    comercio: ComercioData
    timestamp: str

class CategoriaCreadaPayload(BaseModel):
    categoria: CategoriaData
    timestamp: str
    