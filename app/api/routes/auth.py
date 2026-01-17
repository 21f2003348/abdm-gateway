from fastapi import APIRouter, HTTPException, status, Depends

from app.api.schemas import SessionRequest, SessionResponse
from app.services.auth_service import validate_client_credentials, issue_access_token
from app.deps.headers import require_gateway_headers
from app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/session", response_model=SessionResponse)
def create_session(
    body: SessionRequest, 
    headers=Depends(require_gateway_headers),
    db: Session = Depends(get_db)
):
    if not validate_client_credentials(db, body.clientId, body.clientSecret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials"
        )

    if body.grantType != "client_credentials":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only client_credentials grant type is supported"
        )
    
    token_data = issue_access_token(db, body.clientId, headers["cm_id"])
    return SessionResponse(**token_data)

@router.get("/certs")
def get_certs():
    """Placeholder for public certificates endpoint"""
    return {
        "keys": [
            {
                "kty": "RSA",
                "use": "sig",
                "kid": "demo-key-1",
                "alg": "RS256",
                "n": "placeholder",
                "e": "AQAB"
            }
        ]
    }