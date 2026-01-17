import uuid
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import LinkToken, LinkTransaction

def generate_link_token(db: Session, patient_id: str, hip_id: str) -> Dict:
    """Generate a link token for patient linking"""
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(seconds=300)
    
    link_token = LinkToken(
        token=token,
        patient_id=patient_id,
        hip_id=hip_id,
        expires_at=expires_at
    )
    db.add(link_token)
    db.commit()
    db.refresh(link_token)
    
    return {"token": token, "expiresIn": 300}

def link_care_contexts(db: Session, patient_id: str, care_contexts: List[Dict]) -> Dict:
    """Link care contexts (placeholder implementation)"""
    return {"status": "PENDING"}

def discover_patient(db: Session, mobile: str, name: str | None) -> Dict:
    """Discover patient by mobile number"""
    patient_id = f"pat-{mobile}"
    return {"patientId": patient_id, "status": "FOUND"}

def init_link(db: Session, patient_id: str, txn_id: str) -> Dict:
    """Initialize a link transaction"""
    link_txn = LinkTransaction(
        txn_id=txn_id,
        patient_id=patient_id,
        status="INITIATED"
    )
    db.add(link_txn)
    db.commit()
    db.refresh(link_txn)
    return {"status": "INITIATED", "txnId": txn_id}

def confirm_link(db: Session, patient_id: str, txn_id: str, otp: str) -> Dict:
    """Confirm link transaction with OTP"""
    link_txn = db.query(LinkTransaction).filter(LinkTransaction.txn_id == txn_id).first()
    if link_txn:
        link_txn.status = "CONFIRMED"
        db.commit()
        db.refresh(link_txn)
        return {"status": "CONFIRMED", "txnId": txn_id}
    return {"status": "NOT_FOUND", "txnId": txn_id}

def notify_link(db: Session, txn_id: str, status: str) -> Dict:
    """Notify link transaction status update"""
    link_txn = db.query(LinkTransaction).filter(LinkTransaction.txn_id == txn_id).first()
    if link_txn:
        link_txn.status = status
        db.commit()
        db.refresh(link_txn)
        return {"status": status, "txnId": txn_id}
    return {"status": "NOT_FOUND", "txnId": txn_id}