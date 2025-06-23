from sqlalchemy.orm import Session
from app.guilds.blockchain.schemas.star_schema import DimUser, DimStatus, DimDate, DimConcept
from datetime import datetime

def ensure_user(db: Session, email: str) -> DimUser:
    """Get or create user dimension"""
    user = db.query(DimUser).filter(DimUser.email == email).first()
    if not user:
        user = DimUser(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def ensure_status(db: Session, status_name: str) -> DimStatus:
    """Get or create status dimension"""
    status = db.query(DimStatus).filter(DimStatus.status == status_name).first()
    if not status:
        status = DimStatus(status=status_name)
        db.add(status)
        db.commit()
        db.refresh(status)
    return status

def ensure_date(db: Session, date: datetime) -> DimDate:
    """Get or create date dimension with proper date attributes"""
    # Normalize to start of day for consistency
    normalized_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    date_dim = db.query(DimDate).filter(DimDate.date == normalized_date).first()
    if not date_dim:
        date_dim = DimDate(
            date=normalized_date,
            year=normalized_date.year,
            month=normalized_date.month,
            day=normalized_date.day
        )
        db.add(date_dim)
        db.commit()
        db.refresh(date_dim)
    return date_dim

def ensure_concept(db: Session, concept_name: str) -> DimConcept:
    """Get or create concept dimension"""
    concept = db.query(DimConcept).filter(DimConcept.concept == concept_name).first()
    if not concept:
        concept = DimConcept(concept=concept_name)
        db.add(concept)
        db.commit()
        db.refresh(concept)
    return concept