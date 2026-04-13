import os
from datetime import datetime, timedelta
from typing import Optional

import jwt as pyjwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.orm import Session

# ── 상수 ──────────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7일

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT 액세스 토큰을 생성합니다.

    Args:
        data: 토큰에 포함할 페이로드 (예: {"sub": "user@email.com"})
        expires_delta: 만료 기간 (기본: 7일)

    Returns:
        서명된 JWT 토큰 문자열
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_google_token(token: str) -> dict:
    """
    Google OAuth2 ID 토큰을 검증하고 사용자 정보를 반환합니다.
    환경변수 GOOGLE_CLIENT_ID가 설정되어 있지 않으면 개발용 모드로 동작합니다.

    Args:
        token: Google로부터 전달받은 ID 토큰

    Returns:
        검증된 사용자 정보 딕셔너리 (email, name, email_verified 포함)

    Raises:
        HTTPException 401: 토큰 검증 실패 시
    """
    DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    # 개발 모드: GOOGLE_CLIENT_ID 미설정 시 이메일 문자열 직접 처리
    if not GOOGLE_CLIENT_ID and isinstance(token, str) and "@" in token:
        return {"email": token, "name": token.split("@")[0], "email_verified": True}

    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        return idinfo
    except Exception as e:
        if DEBUG:
            # 개발 환경: 서명 검증 없이 페이로드 추출 시도
            try:
                payload = pyjwt.decode(token, options={"verify_signature": False})
                if payload.get("email"):
                    return payload
            except pyjwt.PyJWTError:
                pass
            if isinstance(token, str) and "@" in token:
                return {"email": token, "name": token.split("@")[0], "email_verified": True}

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_jwt(token: str) -> dict:
    """
    JWT 토큰을 디코딩하여 페이로드를 반환합니다.

    Raises:
        HTTPException 401: 디코딩 실패 시
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except pyjwt.PyJWTError:
        raise credentials_exception
