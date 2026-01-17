from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.db.models import Bridge, BridgeService
import uuid

def register_bridge(db: Session, bridge_id: str, entity_type: str, name: str) -> Dict:
    """Register a new bridge or return existing one"""
    try:
        bridge = db.query(Bridge).filter(Bridge.bridge_id == bridge_id).first()
        
        if not bridge:
            bridge = Bridge(
                bridge_id=bridge_id,
                entity_type=entity_type,
                name=name,
                webhook_url=None
            )
            db.add(bridge)
            db.flush()  # Flush to get bridge ID
            
            # Create default services only if bridge is new
            for i in range(1, 3):
                service = BridgeService(
                    service_id=f"{bridge_id}-svc-{i}",
                    bridge_id=bridge_id,
                    name=f"Service-{i}",
                    active=True,
                    version="v1"
                )
                db.add(service)
            
            try:
                db.commit()
            except Exception as e:
                db.rollback()
                raise e
            
            db.refresh(bridge)
        else:
            # Bridge exists, just refresh to get latest data
            db.refresh(bridge)
        
        # Get services (whether bridge is new or existing)
        services = db.query(BridgeService).filter(BridgeService.bridge_id == bridge_id).all()
        
        return {
            "bridgeId": bridge.bridge_id,
            "entityType": bridge.entity_type,
            "name": bridge.name,
            "webhookUrl": bridge.webhook_url,
            "services": [
                {
                    "id": svc.service_id,
                    "name": svc.name,
                    "active": svc.active,
                    "version": svc.version
                }
                for svc in services
            ]
        }
    except Exception as e:
        # Rollback on any error
        db.rollback()
        raise e

def update_bridge_url(db: Session, bridge_id: str, url: str) -> Optional[Dict]:
    """Update bridge webhook URL"""
    bridge = db.query(Bridge).filter(Bridge.bridge_id == bridge_id).first()
    if bridge:
        bridge.webhook_url = url
        db.commit()
        db.refresh(bridge)
        return {"bridgeId": bridge.bridge_id, "webhookUrl": bridge.webhook_url}
    return None

def get_services_by_bridge(db: Session, bridge_id: str) -> List[Dict]:
    """Get all services for a bridge"""
    services = db.query(BridgeService).filter(BridgeService.bridge_id == bridge_id).all()
    return [
        {
            "id": svc.service_id,
            "name": svc.name,
            "active": svc.active,
            "version": svc.version
        }
        for svc in services
    ]

def get_service_by_id(db: Session, service_id: str) -> Optional[Dict]:
    """Get service by ID"""
    service = db.query(BridgeService).filter(BridgeService.service_id == service_id).first()
    if service:
        return {
            "id": service.service_id,
            "name": service.name,
            "active": service.active,
            "version": service.version
        }
    return None