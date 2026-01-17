from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps.headers import require_gateway_headers
from app.deps.auth import get_current_token
from app.db.database import get_db
from app.api.schemas import (
    ConsentInitRequest, ConsentInitResponse,
    ConsentStatusResponse,
    ConsentFetchRequest, ConsentFetchResponse,
    ConsentNotifyRequest
)
from app.services.consent_service import (
    init_consent, get_consent_status,
    fetch_consent, notify_consent
)

router = APIRouter(prefix="/consent", tags=["consent"])

@router.post("/init", response_model=ConsentInitResponse)
def init_consent_endpoint(body: ConsentInitRequest,
                          token=Depends(get_current_token),
                          headers=Depends(require_gateway_headers),
                          db: Session = Depends(get_db)):
    return ConsentInitResponse(**init_consent(db, body.patientId, body.hipId, body.purpose.dict()))

@router.get("/status/{consentRequestId}", response_model=ConsentStatusResponse)
def get_status_endpoint(consentRequestId: str,
                        token=Depends(get_current_token),
                        headers=Depends(require_gateway_headers),
                        db: Session = Depends(get_db)):
    consent = get_consent_status(db, consentRequestId)
    if not consent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consent request not found")
    return ConsentStatusResponse(**consent)

@router.post("/fetch", response_model=ConsentFetchResponse)
def fetch_consent_endpoint(body: ConsentFetchRequest,
                           token=Depends(get_current_token),
                           headers=Depends(require_gateway_headers),
                           db: Session = Depends(get_db)):
    consent = fetch_consent(db, body.consentRequestId)
    if not consent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consent not found")
    return ConsentFetchResponse(**consent)

@router.post("/notify")
def notify_consent_endpoint(body: ConsentNotifyRequest,
                            db: Session = Depends(get_db)):
    return notify_consent(db, body.consentRequestId, body.status)