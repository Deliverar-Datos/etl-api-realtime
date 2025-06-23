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
    TENANT_CREAR = "tenant.crear"
    COMERCIO_CREAR = "comercio.crear"
    CATEGORIA_CREAR = "categoria.crear"


class CallbackRequest(BaseModel):
    topic: EventTopic
    payload: Optional[dict] = None

