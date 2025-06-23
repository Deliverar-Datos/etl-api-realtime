from sqlalchemy.orm import Session
from app.guilds.blockchain.services.dimension_helpers import ensure_user, ensure_status, ensure_date, ensure_concept
from app.guilds.blockchain.schemas.star_schema import FactTransaction
from app.guilds.blockchain.schemas.events import CryptoPaymentData

class PaymentProcessor:
    @staticmethod
    def process(db: Session, data: CryptoPaymentData):
        """Process crypto payment events"""
        try:
            # Process dimensions
            from_user = ensure_user(db, data.fromEmail)
            to_user = ensure_user(db, data.toEmail)
            status = ensure_status(db, data.status)
            date = ensure_date(db, data.transactionDate)
            concept = ensure_concept(db, data.concept)
            
            # Create fact
            transaction = FactTransaction(
                transaction_id=data.transactionId,
                event_type="payment",
                status_id=status.id,
                blockchain_tx_hash=data.blockchainTxHash,
                transaction_date=data.transactionDate,
                date_id=date.id,
                amount=float(data.amount),
                concept_id=concept.id,
                from_user_id=from_user.id,
                to_user_id=to_user.id,
                email_user_id=from_user.id
            )
            
            db.add(transaction)
            db.commit()
            return transaction
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing payment: {str(e)}")