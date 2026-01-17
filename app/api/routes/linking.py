from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps.headers import require_gateway_headers
from app.deps.auth import get_current_token
from app.db.database import get_db
from app.api.schemas import (
    LinkTokenRequest, LinkTokenResponse,
    LinkCareContextRequest, LinkCareContextResponse,
    DiscoverPatientRequest, DiscoverPatientResponse,
    LinkInitRequest, LinkInitResponse,
    LinkConfirmRequest, LinkConfirmResponse,
    LinkNotifyRequest
)
from app.services.linking_service import (
    generate_link_token, link_care_contexts,
    discover_patient, init_link, confirm_link, notify_link
)

router = APIRouter(prefix="/link", tags=["linking"])

@router.post("/token/generate", response_model=LinkTokenResponse)
def generate_token(body: LinkTokenRequest,
                    token=Depends(get_current_token),
                    headers=Depends(require_gateway_headers),
                    db: Session = Depends(get_db)):
    return LinkTokenResponse(**generate_link_token(db, body.patientId, body.hipId))

@router.post("/carecontext", response_model=LinkCareContextResponse)
def link_carecontext(body: LinkCareContextRequest,
                     token=Depends(get_current_token),
                     headers=Depends(require_gateway_headers),
                     db: Session = Depends(get_db)):
    return LinkCareContextResponse(**link_care_contexts(db, body.patientId, [cc.dict() for cc in body.careContexts]))

@router.post("/discover", response_model=DiscoverPatientResponse)
def discover(body: DiscoverPatientRequest,
             token=Depends(get_current_token),
             headers=Depends(require_gateway_headers),
             db: Session = Depends(get_db)):
    return DiscoverPatientResponse(**discover_patient(db, body.mobile, body.name))

@router.post("/init", response_model=LinkInitResponse)
def init(body: LinkInitRequest,
                       token=Depends(get_current_token),
                       headers=Depends(require_gateway_headers),
                       db: Session = Depends(get_db)):
    return LinkInitResponse(**init_link(db, body.patientId, body.txnId))

@router.post("/confirm", response_model=LinkConfirmResponse)
def confirm(body: LinkConfirmRequest,
                          token=Depends(get_current_token),
                          headers=Depends(require_gateway_headers),
                          db: Session = Depends(get_db)):
    return LinkConfirmResponse(**confirm_link(db, body.patientId, body.txnId, body.otp))

@router.post("/notify")
def notify(body: LinkNotifyRequest,
           db: Session = Depends(get_db)):
    return notify_link(db, body.txnId, body.status)