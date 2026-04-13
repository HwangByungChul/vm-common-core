from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .jwt_handler import oauth2_scheme, decode_jwt
from ..db.database import get_db
from .models import User, StatusEnum, RoleEnum


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    현재 요청의 JWT 토큰을 검증하고 DB에서 사용자를 반환합니다.
    모든 인증이 필요한 엔드포인트의 Depends로 사용합니다.

    Usage:
        @router.get("/me")
        def get_me(user: User = Depends(get_current_user)):
            return user
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_jwt(token)
    email: str = payload.get("sub")
    if not email:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    ACTIVE 상태의 인증된 사용자를 반환합니다.
    가입 승인이 필요한 서비스에서 사용합니다.

    Usage:
        @router.get("/dashboard")
        def dashboard(user: User = Depends(get_current_active_user)):
            ...
    """
    if current_user.status != StatusEnum.ACTIVE and current_user.role != RoleEnum.SYSTEM:
        raise HTTPException(status_code=403, detail="Inactive or pending user")
    return current_user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    ADMIN 또는 SYSTEM 권한의 사용자를 반환합니다.
    관리자 전용 엔드포인트에 사용합니다.

    Usage:
        @router.delete("/users/{user_id}")
        def delete_user(user_id: int, admin: User = Depends(get_admin_user)):
            ...
    """
    if current_user.role not in [RoleEnum.ADMIN, RoleEnum.SYSTEM]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user
