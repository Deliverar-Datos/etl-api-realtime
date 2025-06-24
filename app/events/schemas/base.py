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

    ## Backoffice
    IVA_PEDIDO = "iva.pedido"
    IVA_RESPUESTA = "iva.respuesta"


class CallbackRequest(BaseModel):
    topic: EventTopic
    payload: Optional[dict] = None

