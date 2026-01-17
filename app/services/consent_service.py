import uuid 
from typing import Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models import Consent

def init_consent(db: Session, patient_id: str, hip_id: str, purpose: Dict) -> Dict:
    """Initialize a consent request"""
    consent_id = str(uuid.uuid4())
    consent = Consent(
        consent_request_id=consent_id,
        patient_id=patient_id,
        hip_id=hip_id,
        purpose=purpose,
        status="REQUESTED",
        granted_at=None
    )
    db.add(consent)
    db.commit()
    db.refresh(consent)
    return {"consentRequestId": consent_id, "status": "REQUESTED"}

def get_consent_status(db: Session, consent_id: str) -> Optional[Dict]:
    """Get consent status"""
    consent = db.query(Consent).filter(Consent.consent_request_id == consent_id).first()
    if consent:
        return {
            "consentRequestId": consent_id,
            "status": consent.status,
            "grantedAt": consent.granted_at.isoformat() if consent.granted_at else None
        }
    return None

def fetch_consent(db: Session, consent_id: str) -> Optional[Dict]:
    """Fetch consent artefact"""
    consent = db.query(Consent).filter(Consent.consent_request_id == consent_id).first()
    if consent:
        return {
            "consentRequestId": consent_id,
            "status": consent.status,
            "consentArtefact": {"data": consent.consent_artefact} if consent.consent_artefact else None
        }
    return None

def notify_consent(db: Session, consent_id: str, status: str) -> Dict:
    """Notify consent status update"""
    consent = db.query(Consent).filter(Consent.consent_request_id == consent_id).first()
    if consent:
        consent.status = status
        if status == "GRANTED":
            consent.granted_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(consent)
        return {"consentRequestId": consent_id, "status": status}
    return {"consentRequestId": consent_id, "status": "NOT_FOUND"}
