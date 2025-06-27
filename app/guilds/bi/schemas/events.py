from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union

# 1. Cliente se registra
class ClientRegisteredData(BaseModel):
    clientId: int
    name: str = Field(..., max_length=20)
    surname: str = Field(..., max_length=20)
    email: Union[str, None] = Field(None, max_length=40)
    signUpDate: datetime = Field(...)

# 2. Delivery se registra o se actualiza
class DeliveryRegisteredData(BaseModel):
    deliveryId: int
    name: str = Field(..., max_length=20)
    surname: str = Field(..., max_length=20)
    email: Union[str, None] = Field(None, max_length=40)
    signUpDate: datetime = Field(...)
    totalSalary: Union[int, float]

# 3. Se crea una orden
class OrderRegisteredData(BaseModel):
    orderId: int
    clientId: int
    deliveryId: Optional[int] = None
    statusBefore: str
    statusAfter: str
    date: datetime
    startDelivery: Optional[datetime] = None
    endDelivery: Optional[datetime] = None
    comission: Union[int, float]
    promoId: Optional[int] = None

# 4. Se registra una transacción en la blockchain
class BlockchainTransactionRegisteredData(BaseModel):
    transactionId: int
    date: datetime
    clientId: Optional[int] = None
    amount: Union[int, float]
    currency: str = Field(..., max_length=20)
    concept: str
    status: str

# 5. Se registra un tenant (Marketplace)
class TenantRegisteredData(BaseModel):
    tenantId: int
    nombre: str = Field(..., max_length=50)
    razonSocial: str = Field(..., max_length=50)

# 6. Se registra un comercio
class CommerceRegisteredData(BaseModel):
    commerceId: int
    name: str = Field(..., max_length=50)
    postCode: int = Field(...)
    tenantId: int = Field(...)

# 7. Promoción creada con toda la información relacionada
class FullPromoRegisteredData(BaseModel):
    promocion_id: int = Field(...)
    nombre: str = Field(..., max_length=20)
    tipo_descuento: str = Field(..., max_length=20)
    valor_descuento: Union[int, float]
    productos_afectados: List[int] = Field(...)
    fecha_inicio: datetime = Field(...)
    fecha_fin: datetime = Field(...)
    tenant_id: Optional[int] = None
    comercio_id: Optional[int] = None

# 8. Actualización de estado de orden
class OrderStatusUpdatedData(BaseModel):
    orden_id: int = Field(...)
    estado_anterior: str = Field(..., max_length=50)
    estado_nuevo: str = Field(..., max_length=50)
    fecha_actualizacion: datetime = Field(...)

# 9. Asociación de promoción a comercio
class PromoCommerceLinkedData(BaseModel):
    promoId: int
    commerceId: int

# 10. Asociación de promoción a tenant
class PromoTenantLinkedData(BaseModel):
    promoId: int
    tenantId: int
