import uuid 
from typing import Dict, Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models import HealthData, DataRequest

def send_health_info(db: Session, txn_id: str, patient_id: str, hip_id: str, care_context_id: str, health_info: Dict, metadata: Dict):
    """Store health information data"""
    health_data = HealthData(
        txn_id=txn_id,
        patient_id=patient_id,
        hip_id=hip_id,
        care_context_id=care_context_id,
        health_info=health_info,
        health_metadata=metadata,  # Using health_metadata column name
        status="RECEIVED"
    )
    db.add(health_data)
    db.commit()
    db.refresh(health_data)
    return {"status": "RECEIVED", "txnId": txn_id}

def request_health_info(db: Session, patient_id: str, hip_id: str, care_context_id: str, data_types: List[str]) -> Dict:
    """Create a health information request"""
    request_id = str(uuid.uuid4())
    data_request = DataRequest(
        request_id=request_id,
        patient_id=patient_id,
        hip_id=hip_id,
        care_context_id=care_context_id,
        data_types=data_types,
        status="REQUESTED"
    )
    db.add(data_request)
    db.commit()
    db.refresh(data_request)
    return {"requestId": request_id, "status": "REQUESTED"}

def get_data_request_status(db: Session, request_id: str) -> Optional[Dict]:
    """Get data request status"""
    data_request = db.query(DataRequest).filter(DataRequest.request_id == request_id).first()
    if data_request:
        return {
            "requestId": data_request.request_id,
            "patientId": data_request.patient_id,
            "hipId": data_request.hip_id,
            "careContextId": data_request.care_context_id,
            "dataTypes": data_request.data_types,
            "status": data_request.status,
            "requestedAt": data_request.requested_at.isoformat() if data_request.requested_at else None
        }
    return None

def notify_data_flow(db: Session, txn_id: str, status: str, hip_id: str) -> Dict:
    """Notify data flow status update"""
    health_data = db.query(HealthData).filter(HealthData.txn_id == txn_id).first()
    if health_data:
        health_data.status = status
        db.commit()
        db.refresh(health_data)
    return {"status": "ACKNOWLEDGED"}
