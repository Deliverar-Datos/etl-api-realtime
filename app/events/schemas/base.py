from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventTopic(str, Enum):
    ## Blockchain
    CRYPTO_PAYMENT = "crypto.payment"
    BUY_CRYPTO = "buy.crypto"
    SELL_CRYPTO = "sell.crypto"
    
    ## Marketplace
    TENANT_CREADO = "tenant.creado"
    COMERCIO_CREADO = "comercio.creado"
    CATEGORIA_CREADA = "categoria.creada"

    BI_TEST = "bi.test"

    ## Repartidor
    PEDIDO_ACEPTADO = "pedido.aceptado"
    PEDIDO_ASIGNADO = "pedido.asignado"
    PEDIDO_ENTREGADO = "pedido.entregado"
    PEDIDO_ARRIBO = "pedido.arribo"
    DELIVERY_NUEVOREPARTIDOR = "delivery.nuevoRepartidor"
    PEDIDO_ENCAMINO = "pedido.enCamino"


class CallbackRequest(BaseModel):
    body: Optional[dict] = None
