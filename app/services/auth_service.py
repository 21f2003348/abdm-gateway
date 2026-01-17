from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.security import create_access_token
from app.db.models import Client

settings = get_settings()

def validate_client_credentials(db: Session, client_id: str, client_secret: str) -> bool:
    """Validate client credentials against database"""
    client = db.query(Client).filter(
        Client.client_id == client_id,
        Client.client_secret == client_secret,
        Client.is_active == True
    ).first()
    return client is not None

def issue_access_token(db: Session, client_id: str, cm_id: str) -> dict:
    """Issue access token for authenticated client"""
    token = create_access_token({"clientId": client_id, "cmId": cm_id})
    return {
        "accessToken": token,
        "expiresIn": settings.jwt_expiry_seconds,
        "tokenType": "Bearer"
    }