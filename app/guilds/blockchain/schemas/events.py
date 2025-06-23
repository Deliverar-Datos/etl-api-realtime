from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.events.schemas.base import EventTopic

class CryptoPaymentData(BaseModel):
    transactionId: str
    fromEmail: str = Field(..., max_length=254)
    toEmail: str = Field(..., max_length=254)
    amount: str
    concept: str
    status: str
    blockchainTxHash: str
    transactionDate: datetime

class BuySellCryptoData(BaseModel):
    transactionId: str
    email: str = Field(..., max_length=254)
    cryptoAmount: str
    fiatAmount: str
    status: str
    blockchainTxHash: str
    transactionDate: datetime
    topic: Optional[EventTopic] = None  # Will be set by the router