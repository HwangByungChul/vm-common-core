from sqlalchemy import Column, DateTime
from datetime import datetime

from .database import Base


class TimestampMixin:
    """
    created_at, updated_at 컬럼을 자동으로 추가하는 Mixin 클래스.
    모든 모델에 공통으로 적용하여 생성/수정 시각을 자동 기록합니다.

    Usage:
        class MyModel(Base, TimestampMixin):
            __tablename__ = "my_table"
            id = Column(Integer, primary_key=True)
            ...
    """
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
