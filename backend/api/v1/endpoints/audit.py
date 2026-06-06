from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from backend.database.session import get_db
from backend.database.models import AuditLog, User
from backend.api.v1.dependencies import require_role

router = APIRouter()

@router.get("/logs")
def get_audit_logs(
    limit: int = 50,
    action_type: str = None,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db)
):
    """
    Retrieve system audit logs for tracking database state mutations. Restricted to admins.
    """
    query = db.query(AuditLog)
    if action_type:
        query = query.filter(AuditLog.action_type == action_type)
        
    logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action_type": log.action_type,
            "ip_address": log.ip_address,
            "before_state": log.before_state,
            "after_state": log.after_state,
            "timestamp": log.timestamp
        }
        for log in logs
    ]
