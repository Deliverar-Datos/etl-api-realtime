from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventTopic(str, Enum):
    ## Blockchain
    CRYPTO_PAYMENT = "crypto.payment"
    BUY_CRYPTO = "buy.crypto"
    SELL_CRYPTO = "sell.crypto"


class CallbackRequest(BaseModel):
    topic: EventTopic
    data: dict
