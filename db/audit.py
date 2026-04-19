from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from .database import Base
from .base_model import TimestampMixin

class AuditLog(Base, TimestampMixin):
    """
    시스템 전반의 주요 변경 사항이나 사용자 활동을 기록하는 공통 감사 로그 모델.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)  # 로그를 남긴 사용자 ID (또는 이메일)
    action = Column(String, index=True, nullable=False) # 수행된 작업 (예: "UPDATE_PORTFOLIO", "LOGIN")
    target_type = Column(String, index=True)            # 대상 엔티티 타입 (예: "Stock", "User")
    target_id = Column(String, index=True)              # 대상 엔티티 ID
    details = Column(JSON, nullable=True)               # 상세 변경 내용 (JSON 포맷)
    ip_address = Column(String, nullable=True)          # 요청 IP 주소
    status = Column(String, default="SUCCESS")          # 작업 결과 상태 (SUCCESS, FAIL)
