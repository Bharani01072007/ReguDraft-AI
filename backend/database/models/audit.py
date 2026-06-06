import uuid
from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action_type = Column(String(100), nullable=False)  # "LOGIN", "CREATE_PROJECT", "GENERATE_DRAFT", "APPROVE_DRAFT", "REJECT_DRAFT", "UPDATE_DRAFT"
    ip_address = Column(String(45), nullable=True)
    before_state = Column(JSON, nullable=True)
    after_state = Column(JSON, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", backref="audit_logs")
