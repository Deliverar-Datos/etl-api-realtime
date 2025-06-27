from app.guilds.bi.schemas.events import BlockchainTransactionRegisteredData
from app.guilds.bi.models.star_schema import DimBlockchainTransactions, DimClient
from sqlalchemy.orm import Session
from datetime import datetime
from app.guilds.bi.services.dimension_helpers import ensure_status_transaction, ensure_currency, ensure_date, ensure_client

class BlockchainTransactionRegisteredProcessor:
    @staticmethod
    def process(db: Session, data: BlockchainTransactionRegisteredData):
        try:
            status = ensure_status_transaction(db, data.status)
            currency = ensure_currency(db, data.currency)
            date = ensure_date(db, data.date)
            client = None
            if data.clientId:
                # Assuming client details are not available here, just linking by ID
                # If client details are needed, ensure_client would need more parameters
                client = ensure_client(db, data.clientId) 

            transaction = db.query(DimBlockchainTransactions).filter_by(transaction_id=data.transactionId).first()
            if not transaction:
                transaction = DimBlockchainTransactions(
                    transaction_id=data.transactionId,
                    date_id=date.id,
                    client_id=client.client_id if client else None,
                    amount=data.amount,
                    currency_id=currency.currency_id,
                    concept=data.concept, # concept is now nullable=False in model, so no need for 'or ''
                    status_id=status.id
                )
                db.add(transaction)
            db.commit()
            return transaction

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error processing blockchain transaction for BI: {str(e)}")
