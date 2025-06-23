from app.events.schemas.base import EventTopic
from app.guilds.blockchain.services.dimension_helpers import ensure_date, ensure_status, ensure_user
from app.guilds.blockchain.schemas.star_schema import FactTransaction
from app.guilds.blockchain.schemas.events import BuySellCryptoData
from sqlalchemy.orm import Session

class BlockchainBuySellProcessor:
    @staticmethod
    def process(db: Session, data: BuySellCryptoData):
        """Process buy/sell crypto events"""
        try:
            user = ensure_user(db, data.email)
            status = ensure_status(db, data.status)
            date = ensure_date(db, data.transactionDate)
            
            # Determine event type based on topic
            event_type = "buy_crypto" if data.topic == EventTopic.BUY_CRYPTO else "sell_crypto"
            
            transaction = FactTransaction(
                transaction_id=data.transactionId,
                event_type=event_type,
                status_id=status.id,
                blockchain_tx_hash=data.blockchainTxHash,
                transaction_date=data.transactionDate,
                date_id=date.id,
                fiat_amount=float(data.fiatAmount),
                email_user_id=user.id,
                from_user_id=user.id,
                amount=float(data.fiatAmount)
            )
            
            db.add(transaction)
            db.commit()
            return transaction
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing {data.topic}: {str(e)}")