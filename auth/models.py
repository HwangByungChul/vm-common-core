from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..db.database import Base


class RoleEnum(str, enum.Enum):
    SYSTEM = "SYSTEM"
    ADMIN = "ADMIN"
    USER = "USER"


class StatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    INACTIVE = "INACTIVE"


class User(Base):
    """
    범용 사용자 모델. 어떤 프로젝트에서도 그대로 사용 가능합니다.
    프로젝트별 추가 필드는 User를 상속하거나 별도 테이블로 확장합니다.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING, nullable=False)

    # 선택 기능: 약관 동의, 마지막 로그인
    terms_agreed_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    telegram_chat_id = Column(String(50), nullable=True)

    # 일일 레포트 수신 동의 (알림 시스템 연동)
    receive_daily_report = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
