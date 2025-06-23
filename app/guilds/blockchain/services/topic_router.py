from sqlalchemy.orm import Session
from app.events.schemas.base import EventTopic
from app.guilds.blockchain.schemas.events import CryptoPaymentData, BuySellCryptoData
from .processors.payment_processor import PaymentProcessor
from .processors.buysell_processor import BlockchainBuySellProcessor

class BlockchainTopicRouter:
    @staticmethod
    def route(topic: str, payload: dict, db: Session):
        """Route blockchain events to appropriate processors"""
        try:
            if topic == EventTopic.CRYPTO_PAYMENT:
                print("Crypto Payment")
                data = CryptoPaymentData(**payload)
                return PaymentProcessor.process(db, data)
            elif topic in (EventTopic.BUY_CRYPTO, EventTopic.SELL_CRYPTO):
                data = BuySellCryptoData(**payload)
                data.topic = topic  # Add topic to data for processor
                return BlockchainBuySellProcessor.process(db, data)
            else:
                raise ValueError(f"Unsupported blockchain topic: {topic}")
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing {topic}: {str(e)}")