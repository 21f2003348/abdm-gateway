from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps.headers import require_gateway_headers
from app.deps.auth import get_current_token
from app.db.database import get_db
from app.api.schemas import (
    SendHealthInfoRequest, SendHealthInfoResponse,
    RequestHealthInfoRequest, RequestHealthInfoResponse,
    DataFlowNotifyRequest, DataFlowNotifyResponse,
)
from app.services.data_service import (
    send_health_info, request_health_info,
    get_data_request_status, notify_data_flow
)
router = APIRouter(prefix="/data", tags=["data-transfer"])

@router.post("/health-info", response_model=SendHealthInfoResponse)
def send_health_info_endpoint(body: SendHealthInfoRequest,
                              token=Depends(get_current_token),
                              headers=Depends(require_gateway_headers),
                              db: Session = Depends(get_db)):
    return SendHealthInfoResponse(
        **send_health_info(db, body.txnId, body.patientId, body.hipId,
                           body.careContextId, body.healthInfo.dict(), 
                           body.metadata.dict())
    )

@router.post("/request-info", response_model=RequestHealthInfoResponse)
def request_health_info_endpoint(body: RequestHealthInfoRequest,
                                 token=Depends(get_current_token),
                                 headers=Depends(require_gateway_headers),
                                 db: Session = Depends(get_db)):
    return RequestHealthInfoResponse(
        **request_health_info(db, body.patientId, body.hipId,
                              body.careContextId, body.dataTypes)
    )

@router.get("/request/{request_id}")
def get_request_status_endpoint(request_id: str,
                                token: dict = Depends(get_current_token),
                                db: Session = Depends(get_db)):
    request_status = get_data_request_status(db, request_id)
    if not request_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Request not found")
    return request_status

@router.post("/notify", response_model=DataFlowNotifyResponse)
def data_flow_notify_endpoint(body: DataFlowNotifyRequest,
                               db: Session = Depends(get_db)):
    return DataFlowNotifyResponse(
        **notify_data_flow(db, body.txnId, body.status, body.hipId)
    )