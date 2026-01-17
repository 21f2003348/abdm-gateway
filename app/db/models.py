from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.db.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Client(Base):
    """Client credentials for authentication"""
    __tablename__ = "clients"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    client_id = Column(String, unique=True, nullable=False, index=True)
    client_secret = Column(String, nullable=False)
    cm_id = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Bridge(Base):
    """Bridge entities (HIP/HIU)"""
    __tablename__ = "bridges"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    bridge_id = Column(String, unique=True, nullable=False, index=True)
    entity_type = Column(String, nullable=False)  # "HIP" or "HIU"
    name = Column(String, nullable=False)
    webhook_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship
    services = relationship("BridgeService", back_populates="bridge", cascade="all, delete-orphan")

class BridgeService(Base):
    """Services associated with bridges"""
    __tablename__ = "bridge_services"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    service_id = Column(String, unique=True, nullable=False, index=True)
    bridge_id = Column(String, ForeignKey("bridges.bridge_id"), nullable=False)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    version = Column(String, default="v1")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship
    bridge = relationship("Bridge", back_populates="services")

class LinkToken(Base):
    """Link tokens for patient linking"""
    __tablename__ = "link_tokens"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    token = Column(String, unique=True, nullable=False, index=True)
    patient_id = Column(String, nullable=False, index=True)
    hip_id = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())

class LinkTransaction(Base):
    """Link transactions for care context linking"""
    __tablename__ = "link_transactions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    txn_id = Column(String, unique=True, nullable=False, index=True)
    patient_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)  # "INITIATED", "CONFIRMED", etc.
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Consent(Base):
    """Consent requests and artefacts"""
    __tablename__ = "consents"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    consent_request_id = Column(String, unique=True, nullable=False, index=True)
    patient_id = Column(String, nullable=False, index=True)
    hip_id = Column(String, nullable=False)
    purpose = Column(JSON, nullable=False)  # Store purpose as JSON
    data_range = Column(JSON, nullable=True)
    status = Column(String, nullable=False)  # "REQUESTED", "GRANTED", "DENIED", etc.
    granted_at = Column(DateTime, nullable=True)
    consent_artefact = Column(Text, nullable=True)  # Encrypted consent artefact
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class HealthData(Base):
    """Health information data transfers"""
    __tablename__ = "health_data"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    txn_id = Column(String, nullable=False, index=True)
    patient_id = Column(String, nullable=False, index=True)
    hip_id = Column(String, nullable=False)
    care_context_id = Column(String, nullable=False)
    health_info = Column(JSON, nullable=False)  # Encrypted health info
    health_metadata = Column(JSON, nullable=False)  # Renamed from 'metadata' (reserved by SQLAlchemy)
    status = Column(String, default="RECEIVED")  # "RECEIVED", "PROCESSED", etc.
    sent_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class DataRequest(Base):
    """Health information data requests"""
    __tablename__ = "data_requests"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    request_id = Column(String, unique=True, nullable=False, index=True)
    patient_id = Column(String, nullable=False, index=True)
    hip_id = Column(String, nullable=False)
    care_context_id = Column(String, nullable=False)
    data_types = Column(JSON, nullable=False)  # List of data types
    status = Column(String, nullable=False)  # "REQUESTED", "FULFILLED", "FAILED", etc.
    requested_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

